using System.Windows;
using System.Windows.Controls;
namespace Gobblet.Pages;

public partial class MainMenu : Page
{
    public MainMenu()
    {
        InitializeComponent();
    }
    
    private async void StartGame_Click(object sender, RoutedEventArgs e)
    {
        bool hasWeights = await App.Python.AskPythonAsync<bool>("CHECK_WEIGHTS", 
            (data) => data == "true", 5000);

        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(hasWeights ? new TurnChooseMenu() : new LoadingScreen());
    }

    private void Exit_Click(object sender, RoutedEventArgs e)
    {
        Application.Current.Shutdown();
    }
}