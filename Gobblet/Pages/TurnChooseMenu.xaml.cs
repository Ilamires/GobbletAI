using System.Windows;
using System.Windows.Controls;

namespace Gobblet.Pages;

public partial class TurnChooseMenu : Page
{
    public TurnChooseMenu()
    {
        InitializeComponent();
    }

    private void GoFirst_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new GamePage(true));
    }

    private void GoSecond_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new GamePage(false));
    }

    private void BackToMainMenu_Click(object sender, RoutedEventArgs e)
    {

        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new MainMenu());
    }
}