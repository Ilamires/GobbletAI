using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace Gobblet.Pages;

public partial class ResultScreen : Page
{
    private bool isPlayerGoFirst;
    public ResultScreen(string isPlayerWin, bool isPlayerGoFirst)
    {
        InitializeComponent();
        if (isPlayerWin == "0.5")
        {
            ResultText.Foreground = Brushes.Gray;
            ResultText.Text = "Draw";
        }
        else if (isPlayerWin == "-1")
        {
            ResultText.Foreground = Brushes.Red;
            ResultText.Text = "You lose";
        }
        else
        {
            ResultText.Foreground = Brushes.LimeGreen;
            ResultText.Text = "You win!!!";
        }
        
        this.isPlayerGoFirst = isPlayerGoFirst;
    }
    private async void ChooseTurn_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
    }
    private async void RestartGame_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new GamePage(isPlayerGoFirst));
    }
    private void Exit_Click(object sender, RoutedEventArgs e)
    {
        Application.Current.Shutdown();
    }
}