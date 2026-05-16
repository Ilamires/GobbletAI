using System;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;

namespace Gobblet.Pages;

public partial class LoadingScreen : Page
{
    public LoadingScreen()
    {
        InitializeComponent();
        Loaded += LoadingPage_Loaded;
    }
    private async void LoadingPage_Loaded(object sender, RoutedEventArgs e)
    {
        await SimulateTrainingAsync();
    }

    private async Task SimulateTrainingAsync()
    {
        for (int progress = 0; progress <= 100; progress += 10)
        {
            LoadingBar.Value = progress;
            PercentText.Text = $"{progress}%";
                
            await Task.Delay(2000);
        }

        await Task.Delay(500);
            
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
    }
}