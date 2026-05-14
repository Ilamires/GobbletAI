using System.Windows;
using Gobblet.Pages;

namespace Gobblet;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
        MainFrame.Navigate(new MainMenu());
    }
}