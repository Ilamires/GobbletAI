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
        Loaded += AITraining_Loaded;
    }
    private async void AITraining_Loaded(object sender, RoutedEventArgs e)
    {
        await TrainingAsync();
    }

    private async Task TrainingAsync()
    {
        int progress = 0;
        while (progress <= 100)
        {
            LoadingBar.Value = progress;
            PercentText.Text = $"{progress}%";
                
            await Task.Delay(2000);
            progress += 10;
        }

        await Task.Delay(500);
            
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
    }
}