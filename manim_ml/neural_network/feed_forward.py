from manim import *
from manim_ml.neural_network.layers import VGroupNeuralNetworkLayer, ConnectiveLayer

class FeedForwardLayer(VGroupNeuralNetworkLayer):
    """Handles rendering a layer for a neural network"""

    def __init__(self, num_nodes, layer_buffer=SMALL_BUFF/2, node_radius=0.08,
                node_color=BLUE, node_outline_color=WHITE, rectangle_color=WHITE,
                node_spacing=0.3, rectangle_fill_color=BLACK, node_stroke_width=2.0,
                rectangle_stroke_width=2.0, animation_dot_color=RED):
        super(VGroupNeuralNetworkLayer, self).__init__()
        self.num_nodes = num_nodes
        self.layer_buffer = layer_buffer
        self.node_radius = node_radius
        self.node_color = node_color
        self.node_stroke_width = node_stroke_width
        self.node_outline_color = node_outline_color
        self.rectangle_stroke_width = rectangle_stroke_width
        self.rectangle_color = rectangle_color
        self.node_spacing = node_spacing
        self.rectangle_fill_color = rectangle_fill_color
        self.animation_dot_color = animation_dot_color

        self.node_group = VGroup()

        self._construct_neural_network_layer()

    def _construct_neural_network_layer(self):
        """Creates the neural network layer"""
        # Add Nodes
        for node_number in range(self.num_nodes):
            node_object = Circle(radius=self.node_radius, color=self.node_color, 
                                stroke_width=self.node_stroke_width)
            self.node_group.add(node_object)
        # Space the nodes
        # Assumes Vertical orientation
        for node_index, node_object in enumerate(self.node_group):
            location = node_index * self.node_spacing
            node_object.move_to([0, location, 0])
        # Create Surrounding Rectangle
        self.surrounding_rectangle = SurroundingRectangle(self.node_group, color=self.rectangle_color, 
                                                        fill_color=self.rectangle_fill_color, fill_opacity=1.0, 
                                                        buff=self.layer_buffer, stroke_width=self.rectangle_stroke_width)
        # Add the objects to the class
        self.add(self.surrounding_rectangle, self.node_group)

    def make_forward_pass_animation(self):
        # make highlight animation
        succession = Succession(
            ApplyMethod(self.node_group.set_color, self.animation_dot_color, run_time=0.25),
            Wait(1.0),
            ApplyMethod(self.node_group.set_color, self.node_color, run_time=0.25),
        )

        return succession

    @override_animation(Create)
    def _create_animation(self, **kwargs):
        animations = []

        animations.append(Create(self.surrounding_rectangle))

        for node in self.node_group:
            animations.append(Create(node))

        animation_group = AnimationGroup(*animations, lag_ratio=0.0)
        return animation_group

class FeedForwardToFeedForward(ConnectiveLayer):
    """Layer for connecting FeedForward layer to FeedForwardLayer"""

    def __init__(self, input_layer, output_layer, passing_flash=True,
                dot_radius=0.05, animation_dot_color=RED, edge_color=WHITE,
                edge_width=0.5):
        super().__init__(input_layer, output_layer)
        self.passing_flash = passing_flash
        self.edge_color = edge_color
        self.dot_radius = dot_radius
        self.animation_dot_color = animation_dot_color
        self.edge_width = edge_width

        self.edges = self.construct_edges()
        self.add(self.edges)

    def construct_edges(self):
        # Go through each node in the two layers and make a connecting line
        edges = []
        for node_i in self.input_layer.node_group:
            for node_j in self.output_layer.node_group:
                line = Line(node_i.get_center(), node_j.get_center(), 
                            color=self.edge_color, stroke_width=self.edge_width)
                edges.append(line)

        edges = VGroup(*edges)
        return edges

    def make_forward_pass_animation(self, run_time=1):
        """Animation for passing information from one FeedForwardLayer to the next"""
        path_animations = []
        dots = []
        for edge in self.edges:
            dot = Dot(color=self.animation_dot_color, fill_opacity=1.0, radius=self.dot_radius)   
            # Add to dots group
            dots.append(dot)
            # Make the animation
            if self.passing_flash:
                anim = ShowPassingFlash(edge.copy().set_color(self.animation_dot_color), time_width=0.2, run_time=3)
            else:
                anim = MoveAlongPath(dot, edge, run_time=run_time, rate_function=sigmoid)
            path_animations.append(anim)

        if not self.passing_flash:
            dots = VGroup(*dots)
            self.add(dots)

        path_animations = AnimationGroup(*path_animations)

        return path_animations

    @override_animation(Create)
    def _create_animation(self, **kwargs):
        animations = []

        for edge in self.edges:
            animations.append(Create(edge))

        animation_group = AnimationGroup(*animations, lag_ratio=0.0)
        return animation_group
