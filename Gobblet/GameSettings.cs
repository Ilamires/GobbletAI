namespace Gobblet;

public class GameSettings
{
    public bool PlayerGoFirst { get; set; }

    public uint Turn { get; private set; }
    public byte CurrentPlayer { get => (byte)(Turn % 2); }
    public bool IsPlayerTurn
    {
        get => PlayerGoFirst && CurrentPlayer == 1 ||
               !PlayerGoFirst && CurrentPlayer == 0;
    }
    
    public GameSettings(bool playerGoFirst = true)
    {
        PlayerGoFirst = playerGoFirst;
        Turn = 1;
    }

    public void TakeTurn() => ++Turn;
    public void Restart()
    {
        PlayerGoFirst = true;
        Turn = 1;
    }
}