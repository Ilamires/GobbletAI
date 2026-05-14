using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Gobblet.CustomControls;

namespace Gobblet.Pages;

public partial class GamePage : Page
{
    public byte FieldSize { get; } = 3;
    public byte FieldSectionWidth { get; } = 90;

    GameFieldButton[][] FieldButtons;
    public GamePage(bool playerGoFirst)
    {
        InitializeComponent();
        
        FieldButtons = new GameFieldButton[FieldSize][];
        for (int i = 0; i < FieldSize; ++i)
        {
            FieldButtons[i] = new GameFieldButton[FieldSize];
            for (int j = 0; j < FieldSize; ++j)
            {
                FieldButtons[i][j] = new GameFieldButton((byte)i, (byte)j);
                FieldButtons[i][j].Width = FieldSectionWidth;
                FieldButtons[i][j].Height = FieldSectionWidth;
                FieldButtons[i][j].BorderThickness = new System.Windows.Thickness(2);
                FieldButtons[i][j].BorderBrush = Brushes.Black;
                FieldButtons[i][j].Click += TakeTurn_Click;
                FieldButtons[i][j].Opacity = 0.5;
                Grid.SetZIndex(FieldButtons[i][j], 1);
            }
        }
        
        for (int row = 0; row < FieldSize; ++row)
        {
            for (int col = 0; col < FieldSize; ++col)
            {
                Grid.SetRow(FieldButtons[row][col], row);
                Grid.SetColumn(FieldButtons[row][col], col);
                InnerGridCentralField.Children.Add(FieldButtons[row][col]);

            }
        }
    }
    
    public void TakeTurn_Click(object sender, EventArgs e)
    {
        
    }

    private void BackToChooseMenu_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
    }
}