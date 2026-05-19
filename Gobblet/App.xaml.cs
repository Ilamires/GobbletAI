using System.Configuration;
using System.Data;
using System.Windows;

namespace Gobblet;

public partial class App : Application
{
    public static PythonBridge Python { get; } = new PythonBridge();
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);

        Python.OutputReceived += msg => System.Diagnostics.Debug.WriteLine($"[PY] {msg}");
        Python.ErrorReceived += err => System.Diagnostics.Debug.WriteLine($"[PY ERR] {err}");

        Python.Start("../../../../GobbletAI/TestAI.py");
    }

    protected override void OnExit(ExitEventArgs e)
    {
        Python.Dispose();
        base.OnExit(e);
    }
}