using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
using Gobblet.CustomControls;

namespace Gobblet.Pages;

public partial class GamePage : Page
{
    
    GameSettings settings;
    public byte FieldSize { get; } = 3;
    public byte FieldSectionWidth { get; } = 90;
    

    GameFieldButton[][] FieldButtons;
    GameButton[][] FirstPlayerButtons;
    GameButton[][] SecondPlayerButtons;
    GameButton[][][] PlayerButtons;

    GameButton chosenPlayerButton;
    public GamePage(bool playerGoFirst)
    {
        InitializeComponent();
        
        settings = new GameSettings(playerGoFirst);

        setFieldButtons();
        placeFieldButtons();

        FirstPlayerButtons = new GameButton[FieldSize][];
        SecondPlayerButtons = new GameButton[FieldSize][];
        PlayerButtons = new GameButton[][][] { FirstPlayerButtons, SecondPlayerButtons };

        setPlayerButtons(0);
        placePlayerButtons(0);
        setPlayerButtons(1);
        placePlayerButtons(1);
        startGame();
    }

    private async void TakeFirstAITurn()
    {
        string[] result = (await App.Python.AskPythonAsync<string>(
            $"TAKE_AI_TURN", 
            (data) => data, 5000)).Split(' ');
        TakeAITurn(int.Parse(result[0]));
    }

    private async void startGame()
    {
        int order = settings.PlayerGoFirst ? 1 : 0;
        bool isGameStarted = await App.Python.AskPythonAsync<bool>(
            $"START_GAME {order}", (data) => data == "true", 5000);
        if (!isGameStarted)
            throw new System.ApplicationException("Game not started");
        if (!settings.PlayerGoFirst)
            TakeFirstAITurn();
    }

    private void setFieldButtons()
    {
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
    }
    
    private void placeFieldButtons()
    {
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
    
    private void setPlayerButtons(int playerNumber)
    {
        for (int i = 0; i < PlayerButtons[playerNumber].Length; ++i)
        {
            PlayerButtons[playerNumber][i] = new GameButton[2];
            for (int j = 0; j < PlayerButtons[playerNumber][i].Length; ++j)
            {
                PlayerButtons[playerNumber][i][j] =
                    new GameButton(j + 1, (GameButton.GameButtonSizes)(i + 1));
                int buttonSize = 50 + (int)(PlayerButtons[playerNumber][i][j].Size - 1) * 15;
                PlayerButtons[playerNumber][i][j].Width = buttonSize;
                PlayerButtons[playerNumber][i][j].Height = buttonSize;
                PlayerButtons[playerNumber][i][j].ButtonColor = playerNumber == 0 ? Brushes.Blue : Brushes.Orange;
                PlayerButtons[playerNumber][i][j].IsEnabled = (settings.PlayerGoFirst && playerNumber == 0 ||
                                                              !settings.PlayerGoFirst && playerNumber == 1);
                PlayerButtons[playerNumber][i][j].Click += PlayerButton_Click;
            }
        }
    }
    
    private void placePlayerButtons(int playerNumber)
    {
        for (int row = 0; row < PlayerButtons[playerNumber].Length; ++row)
        {
            for (int col = 0; col < PlayerButtons[playerNumber][row].Length; ++col)
            {
                if (settings.PlayerGoFirst && playerNumber == 0 || !settings.PlayerGoFirst && playerNumber == 1)
                {
                    int realRow = PlayerButtons[playerNumber].Length - 1 - row;
                    Grid.SetRow(PlayerButtons[playerNumber][realRow][col], row);
                    Grid.SetColumn(PlayerButtons[playerNumber][realRow][col], col + 1);
                    InnerGridBottomLeft.Children.Add(
                        PlayerButtons[playerNumber][realRow][col]);
                }
                else
                {
                    Grid.SetRow(PlayerButtons[playerNumber][row][col], row);
                    Grid.SetColumn(PlayerButtons[playerNumber][row][col], col);
                    InnerGridTopRight.Children.Add(PlayerButtons[playerNumber][row][col]);
                }
            }
        }
    }
    
    private async void TakeTurn_Click(object sender, EventArgs e)
    {
        if (chosenPlayerButton != null)
        {
            GameFieldButton button = (GameFieldButton)sender;
            bool isValidTurn = await TakeTurn(button);
            if (isValidTurn)
            {
                Grid.SetRow(chosenPlayerButton, button.PositionX);
                Grid.SetColumn(chosenPlayerButton, button.PositionY);
                InnerGridBottomLeft.Children.Remove(chosenPlayerButton);
                chosenPlayerButton.Opacity = 1.0;
                InnerGridCentralField.Children.Add(chosenPlayerButton);
                chosenPlayerButton = null;
            }
        }
    }
    
    private void PlayerButton_Click(object sender, EventArgs e)
    {
        GameButton button = (GameButton)sender;
        if (settings.IsPlayerTurn)
        {
            if (chosenPlayerButton == button)
            {
                chosenPlayerButton = null;
                button.Opacity = 1;
            }
            else
            {
                if (chosenPlayerButton != null)
                    chosenPlayerButton.Opacity = 1;
                chosenPlayerButton = button;
                button.Opacity = 0.3;
            }
        }
    }
    private async Task<bool> TakeTurn(GameFieldButton button)
    {
        bool isValidTurn = await App.Python.AskPythonAsync<bool>(
            $"CHECK_TURN {(button.PositionX * 3 + button.PositionY) * 3 + (int)chosenPlayerButton.Size - 1}", 
            (data) => data == "true", 5000);

        string[] result = null;
        if (isValidTurn)
            result = (await App.Python.AskPythonAsync<string>(
            $"TAKE_TURN {(button.PositionX * 3 + button.PositionY) * 3 + (int)chosenPlayerButton.Size - 1}", 
            (data) => data, 5000)).Split(' ');
        if (isValidTurn)
            settings.TakeTurn();
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        if (result.Length > 1)
        {
            mainWindow?.MainFrame.Navigate(new ResultScreen(result[2]));
        }
        else
        {
            result = (await App.Python.AskPythonAsync<string>(
                $"TAKE_AI_TURN",
                (data) => data, 5000)).Split(' ');
            TakeAITurn(int.Parse(result[0]));
            if (result.Length > 1)
                mainWindow?.MainFrame.Navigate(new ResultScreen(result[2]));
        }
        
        return isValidTurn;
    }
    
    private async void TakeAITurn(int action)
    {
        int cell = action / 3;
        int size = action % 3;
        int playerNumber = settings.PlayerGoFirst ? 1 : 0;
        int j = 0;
        while (PlayerButtons[playerNumber][size][j] == null)
            ++j;
        
        GameFieldButton button = FieldButtons[cell / 3][cell % 3];
        Grid.SetRow(PlayerButtons[playerNumber][size][j], button.PositionX);
        Grid.SetColumn(PlayerButtons[playerNumber][size][j], button.PositionY);
        InnerGridTopRight.Children.Remove(PlayerButtons[playerNumber][size][j]);
        InnerGridCentralField.Children.Add(PlayerButtons[playerNumber][size][j]);
        PlayerButtons[playerNumber][size][j] = null;
        settings.TakeTurn();
    }

    private void BackToChooseMenu_Click(object sender, RoutedEventArgs e)
    {
        MainWindow? mainWindow = Application.Current.MainWindow as MainWindow;
        mainWindow?.MainFrame.Navigate(new TurnChooseMenu());
    }
}