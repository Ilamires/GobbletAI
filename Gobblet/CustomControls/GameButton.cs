namespace Gobblet.CustomControls;

public class GameButton : CircleButton
{
    public enum GameButtonSizes
    {
        None = 0,
        Small = 1, Medium = 2, Big = 3
    }
    public int Number { get; set; }
    public GameButtonSizes Size { get; set; }
    public bool OnField { get; set; }
    public GameButton(int number = 0, GameButtonSizes size = GameButtonSizes.Small)
    {
        Number = number;
        Size = size;
        OnField = false;
    }
}