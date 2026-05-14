using System.Windows;
using System.Windows.Controls;
namespace Gobblet.Pages;

public partial class MainMenu : Page
{
    public MainMenu()
    {
        InitializeComponent();
    }
    
    private void StartGame_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        //mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
    }

    private void Exit_Click(object sender, RoutedEventArgs e)
    {
        Application.Current.Shutdown();
    }
}