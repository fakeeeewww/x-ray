import glob
from mitmproxy import utils, script
from mitmproxy.proxy import config
from . import tservers


def test_load_scripts():
    example_dir = utils.Data(__name__).path("../../examples")
    scripts = glob.glob("%s/*.py" % example_dir)

    tmaster = tservers.TestMaster(config.ProxyConfig())

    for f in scripts:
        if "har_extractor" in f:
            continue
        if "flowwriter" in f:
            f += " -"
        if "iframe_injector" in f:
            f += " foo"  # one argument required
        if "filt" in f:
            f += " ~a"
        if "modify_response_body" in f:
            f += " foo bar"  # two arguments required
        try:
            s = script.Script(f, script.ScriptContext(tmaster))  # Loads the script file.
        except Exception as v:
            if "ImportError" not in str(v):
                raise
        else:
            s.unload()
