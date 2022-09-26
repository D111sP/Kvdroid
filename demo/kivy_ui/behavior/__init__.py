from kivy.lang import Builder
from kivy.properties import (
    ColorProperty,
    ListProperty,
    NumericProperty,
    ReferenceListProperty,
    StringProperty,
    VariableListProperty,
)
from kivy.uix.widget import Widget

Builder.load_string(
    """
#:import RelativeLayout kivy.uix.relativelayout.RelativeLayout


<BackgroundLineBehavior>
    canvas.before:
        PushMatrix
        Rotate:
            angle: self.angle
            origin: self._background_origin
        Color:
            rgba: self.bg_color
        RoundedRectangle:
            group: "Background_instruction"
            size: self.size
            pos: self.pos if not isinstance(self, RelativeLayout) else (0, 0)
            # FIXME: Sometimes the radius has the value [], which get a
            # `GraphicException:
            #     Invalid radius value, must be list of tuples/numerics` error`
            radius: root.radius if root.radius else [0, 0, 0, 0]
            source: root.background
        Color:
            rgba: self.line_color if self.line_color else (0, 0, 0, 0)
        Line:
            width: root.line_width
            rounded_rectangle:
                [ \
                self.x,
                self.y, \
                self.width, \
                self.height, \
                *self.radius, \
                100, \
                ]
        PopMatrix
""",
    filename="BackgroundLineBehavior.kv",
)


class BackgroundLineBehavior(Widget):
    background = StringProperty()
    """
    Background image path.

    :attr:`background` is a :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """

    radius = VariableListProperty([0], length=4)
    """
    Canvas radius.

    .. code-block:: python

        # Top left corner slice.
        MDBoxLayout:
            md_bg_color: app.theme_cls.primary_color
            radius: [25, 0, 0, 0]

    :attr:`radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
    """

    bg_color = ColorProperty([0, 0, 0, 0])
    """
    The background color of the widget (:class:`~kivy.uix.widget.Widget`)
    that will be inherited from the :attr:`BackgroundColorBehavior` class.

    For example:

    .. code-block:: kv

        Widget:
            canvas:
                Color:
                    rgba: 0, 1, 1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

    similar to code:

    .. code-block:: kv

        <MyWidget@BackgroundColorBehavior>
            md_bg_color: 0, 1, 1, 1

    :attr:`md_bg_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `[1, 1, 1, 0]`.
    """

    line_color = ColorProperty([0, 0, 0, 0])
    """
    If a custom value is specified for the `line_color parameter`, the border
    of the specified color will be used to border the widget:

    .. code-block:: kv

        MDBoxLayout:
            size_hint: .5, .2
            md_bg_color: 0, 1, 1, .5
            line_color: 0, 0, 1, 1
            radius: [24, ]

    .. versionadded:: 0.104.2

    :attr:`line_color` is an :class:`~kivy.properties.ColorProperty`
    and defaults to `[0, 0, 0, 0]`.
    """

    line_width = NumericProperty(1)
    """
    Border of the specified width will be used to border the widget.

    .. versionadded:: 1.0.0

    :attr:`line_width` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `1`.
    """

    angle = NumericProperty(0)
    background_origin = ListProperty(None)

    _background_x = NumericProperty(0)
    _background_y = NumericProperty(0)
    _background_origin = ReferenceListProperty(
        _background_x,
        _background_y,
    )

    def __init__(self, **kwarg):
        super().__init__(**kwarg)
        self.bind(pos=self.update_background_origin)

    def update_background_origin(self, *_) -> None:
        if self.background_origin:
            self._background_origin = self.background_origin
        else:
            self._background_origin = self.center