from hitchstory import StoryCollection, BaseEngine, validate, Failure
from hitchstory import GivenDefinition, GivenProperty, InfoDefinition, InfoProperty
from strictyaml import EmptyDict, Str, Map, Optional, Enum, MapPattern, Bool
from hitchstory import no_stacktrace_for, strings_match, json_match
from hitchrunpy import ExamplePythonCode, HitchRunPyException
from commandlib import Command, python, python_bin
from commandlib.exceptions import CommandExitError
from path import Path
import colorama
import socket
import jinja2
import shutil
import shlex
import time
import re


def wait_for_port(port_number: int):
    connector = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    start_time = time.time()
    while not connected:
        try:
            connector.connect(("localhost", port_number))
            time.sleep(0.05)
            connected = True
        except OSError:
            pass
        
        if time.time() - start_time > 4.0:
            break
    if not connected:
        raise Failure(f"Port {port_number} never opened.")


class Engine(BaseEngine):
    """Python engine for running tests."""

    given_definition = GivenDefinition(
        postgres=GivenProperty(Str()),
        files=GivenProperty(
            MapPattern(Str(), Str()),
            inherit_via=GivenProperty.OVERRIDE,
        ),
        html=GivenProperty(
            MapPattern(Str(), Str()),
            inherit_via=GivenProperty.OVERRIDE,
        ),
    )

    info_definition = InfoDefinition(
        status=InfoProperty(schema=Enum(["experimental", "stable"])),
        category=InfoProperty(schema=Enum(["behavior", "runner", "inheritance", "parameterization", "documentation",])),
        docs=InfoProperty(schema=Str()),
    )

    def __init__(self, paths, python_path, rewrite=False, cprofile=False, timeout=5.0):
        self.path = paths
        self._rewrite = rewrite
        self._python_path = python_path
        self._cprofile = cprofile
        self._timeout = timeout
        self._podman_compose = python_bin.podman_compose
        self._podman = Command("podman")

    def set_up(self):
        """Set up the environment ready to run the stories."""
        self.path.q = Path("/tmp/q")
        self.path.state = self.path.gen.joinpath("state")
        self.path.working = self.path.state / "working"
        self.path.website = self.path.gen / "website"
        self.path.tbls = self.path.gen / "tbls"

        self._podman_compose(
            "up", "-d", "postgres"
        ).in_dir(self.path.project).output()
        
        wait_for_port(5432)

        self._podman_compose(
            "exec", "postgres",
            "psql", "-U", "postgres_user", "postgres_db",
            "-c", self.given["postgres"]
        ).output()

        if self.path.q.exists():
            self.path.q.remove()
        if self.path.state.exists():
            self.path.state.rmtree(ignore_errors=True)
        self.path.state.mkdir()
        
        self._included_files = []
        
        for filename, contents in list(self.given.get("files", {}).items()):
            self.path.state.joinpath(filename).write_text(self.given["files"][filename])
            self._included_files.append(self.path.state.joinpath(filename))


        self.python = Command(self._python_path)
    
    def sql(self, cmd, will_output):
        cmd_output = self._podman_compose(
            "exec", "postgres",
            "psql", "-U", "postgres_user", "postgres_db",
            "-c", cmd
        ).output()

        actual_output = "\n".join([line.rstrip() for line in cmd_output.split("\n")])

        try:
            strings_match(will_output, actual_output)
        except Failure:
            if self._rewrite:
                self.current_step.rewrite("will_output").to(actual_output)
            else:
                raise

    def run_tbls(self, will_output):
        actual_output = self._podman(
            "run", "-v", "{}:/work".format(self.path.tbls), "--rm", "-t", "ghcr.io/k1low/tbls",
            "out", "-t", "json", 
            "postgres://postgres_user:postgres_password@localhost:5432/postgres_db?sslmode=disable",
        ).output()

        try:
            json_match(will_output, actual_output)
        except Failure:
            if self._rewrite:
                self.current_step.rewrite("will_output").to(actual_output)
            else:
                raise
        
        self.path.state.joinpath("tbls.json").write_text(actual_output)
        self._included_files.append(self.path.state.joinpath("tbls.json"))
    
    @no_stacktrace_for(CommandExitError)
    def run_sql_file(self, filename):
        sql = self.path.gen.joinpath("state", "working", filename).read_text()
        self._podman_compose(
            "exec", "postgres",
            "psql", "-U", "postgres_user", "postgres_db",
            "-c", sql
        ).output()

    @no_stacktrace_for(AssertionError)
    @no_stacktrace_for(HitchRunPyException)
    @validate(
        code=Str(),
        will_output=Str(),
        raises=Map({Optional("type"): Str(), Optional("message"): Str()}),
    )
    def run(self, code, will_output=None, raises=None):
        self.example_py_code = (
            ExamplePythonCode(self.python, self.path.state)
            .with_terminal_size(160, 160)
            .with_setup_code(self.given.get("setup", ""))
            .include_files(*self._included_files)
            .with_timeout(self._timeout)
        )
        to_run = self.example_py_code.with_code(code)

        if self._cprofile:
            to_run = to_run.with_cprofile(
                self.path.profile.joinpath("{0}.dat".format(self.story.slug))
            )

        result = (
            to_run.expect_exceptions().run() if raises is not None else to_run.run()
        )

        actual_output = result.output

        if will_output is not None:
            try:
                strings_match(will_output, actual_output)
            except Failure:
                if self._rewrite:
                    self.current_step.rewrite("will_output").to(actual_output)
                else:
                    raise

        if raises is not None:
            exception_type = raises.get("type")
            message = raises.get("message")

            try:
                result.exception_was_raised(exception_type)
                exception_message = self._story_friendly_output(
                    result.exception.message
                )
                strings_match(message, exception_message)
            except Failure:
                if self._rewrite:
                    new_raises = raises.copy()
                    new_raises["message"] = exception_message
                    self.current_step.update(raises=new_raises)
                else:
                    raise

    def tear_down(self):
        self._podman_compose("down", "-t", "1").output()
        if self.path.q.exists():
            print(self.path.q.text())
