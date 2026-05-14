using System.Windows.Controls;

namespace Gobblet.CustomControls;

public class GameFieldButton : Button
{
    public byte PositionX { get; private set; }
    public byte PositionY { get; private set; }
    
    public GameFieldButton(byte positionX, byte positionY)
    {
        PositionX = positionX;
        PositionY = positionY;
    }
}