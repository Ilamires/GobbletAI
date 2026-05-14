using System.Windows;
using System.Windows.Controls;

namespace Gobblet.Pages;

public partial class GamePage : Page
{
    public GamePage(bool isPlayerGoFirst)
    {
        InitializeComponent();
    }
    private void BackToChooseMenu_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
    }
}