using System;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Globalization;

namespace Gobblet.Pages;

public partial class LoadingScreen : Page
{
    public LoadingScreen()
    {
        InitializeComponent();
        Loaded += AITraining_Loaded;
    }
    private async void AITraining_Loaded(object sender, RoutedEventArgs e)
    {
        await TrainingAsync();
    }

    private async Task TrainingAsync()
    {
        Console.WriteLine(1);
        App.Python.OutputReceived += OnAITrainingOutput;
        App.Python.SendToPython("START_TRAINING_IF_NEEDED");
        Console.WriteLine(3);
    }
    
    private void OnAITrainingOutput(string data)
    {
        Console.WriteLine(2);
        if (data.StartsWith("PROGRESS "))
        {
            Console.WriteLine(data);
            var parts = data.Split(' ');
            if (parts.Length == 2 && double.TryParse(parts[1], CultureInfo.InvariantCulture, out double percent))
            {
                Dispatcher.Invoke(() =>
                {
                    LoadingBar.Value = percent;
                    PercentText.Text = $"{percent:F1}%";
                });
            }
        }
        else if (data == "TRAINING_FINISHED")
        {
            Dispatcher.Invoke(() =>
            {
                App.Python.OutputReceived -= OnAITrainingOutput;
                MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
                mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
            });
        }
    }
}