using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace Gobblet;

public class PythonBridge
{
    private Process pythonProcess;
    
    public event Action<string>? OutputReceived;
    public event Action<string>? ErrorReceived;
    
    public void Start(string scriptPath)
    {
        if (pythonProcess != null) throw new InvalidOperationException("Process already running.");

        var startInfo = new ProcessStartInfo
        {
            FileName = RuntimeInformation.IsOSPlatform(OSPlatform.Windows) ? "python" : "python3",
            Arguments = $"\"{Path.GetFullPath(scriptPath)}\"",
            WorkingDirectory = Path.GetDirectoryName(Path.GetFullPath(scriptPath)),
            
            RedirectStandardInput = true,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,
            CreateNoWindow = true,
            StandardOutputEncoding = Encoding.UTF8,
            StandardErrorEncoding = Encoding.UTF8
        };

        pythonProcess = new Process { StartInfo = startInfo };
        pythonProcess.EnableRaisingEvents = true;
        pythonProcess.Exited += (s, e) => Dispose();

        pythonProcess.OutputDataReceived += (s, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
                OutputReceived?.Invoke(e.Data);
        };

        pythonProcess.ErrorDataReceived += (s, e) =>
        {
            if (!string.IsNullOrEmpty(e.Data))
                ErrorReceived?.Invoke(e.Data);
        };

        pythonProcess.Start();
        pythonProcess.BeginOutputReadLine();
        pythonProcess.BeginErrorReadLine();
    }
    
    public void SendToPython(string message)
    {
        if (pythonProcess?.StandardInput == null || pythonProcess.HasExited) return;
        
        pythonProcess.StandardInput.WriteLine(message);
        pythonProcess.StandardInput.Flush();
    }

    public void Dispose()
    {
        if (pythonProcess == null) return;
        try
        {
            if (!pythonProcess.HasExited)
            {
                pythonProcess.StandardInput.Close();
                pythonProcess.Kill();
                pythonProcess.WaitForExit(2000);
            }
        }
        finally
        {
            pythonProcess?.Dispose();
            pythonProcess = null;
        }
    }
}