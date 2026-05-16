using System.Windows.Controls;
using System.Windows.Media;
using System.Windows;

namespace Gobblet.CustomControls;

public class CircleButton : Button
{
    static CircleButton()
    {
        DefaultStyleKeyProperty.OverrideMetadata(typeof(CircleButton),
            new FrameworkPropertyMetadata(typeof(CircleButton)));
    }

    public Brush ButtonColor
    {
        get { return (Brush)GetValue(ButtonColorProperty); }
        set { SetValue(ButtonColorProperty, value); }
    }

    public static readonly DependencyProperty ButtonColorProperty = DependencyProperty.Register(
        "ButtonColor", typeof(Brush), typeof(CircleButton), new PropertyMetadata(Brushes.Gray));

}