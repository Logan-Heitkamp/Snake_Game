import super_snake as ss
import pytest
from unittest.mock import patch, MagicMock


class TestAppleSpawn:
    def test_apple_spawn(self):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_apples = [[0, 0]]
        for apple in ss.apple_spawn(test_position, test_apples.copy()):
            assert apple not in test_position + test_apples

    # TODO make work
    @patch('super_snake.random.randint')
    @pytest.mark.skip
    def test_apple_spawn_spawn_on_snake(self, mock_randint):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_apples = [[0, 0]]

        mock_randint.return_value = 1

        with ss.apple_spawn(test_position, test_apples.copy()):
            with pytest.raises(TimeoutError):
                ss.apple_spawn(test_position, test_apples.copy())

    # TODO make work
    @patch('super_snake.random.randint')
    @pytest.mark.skip
    def test_apple_spawn_spawn_on_apple(self, mock_randint):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_apples = [[0, 0], [3, 3]]

        mock_randint.return_value = 3

        with ss.apple_spawn(test_position, test_apples.copy()):
            with pytest.raises(TimeoutError):
                ss.apple_spawn(test_position, test_apples.copy())

    def test_apple_spawn_no_apple(self):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_apples = []
        with pytest.raises(ValueError):
            ss.apple_spawn(test_position, test_apples)

    def test_apple_spawn_no_apple_collision(self):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_apples = [[3, 3]]
        with pytest.raises(ValueError):
            ss.apple_spawn(test_position, test_apples)


class TestCheckCollision:
    def test_check_collision_no_collision(self):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_apples = [[3, 3]]

        assert ss.check_collision(test_position, test_apples) == 0

    def test_check_collision_apple_collision(self):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_apples = [[0, 0]]

        assert ss.check_collision(test_position, test_apples) == 2

    def test_check_collision_body_collision(self):
        test_position = [[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]
        test_apples = [[3, 3]]

        assert ss.check_collision(test_position, test_apples) == 1

    def test_check_collision_top_wall_collision(self):
        test_position = [[0, -1], [0, 0], [0, 1], [1, 0]]
        test_apples = [[3, 3]]

        assert ss.check_collision(test_position, test_apples) == 1

    def test_check_collision_left_wall_collision(self):
        test_position = [[-1, 0], [0, 0], [0, 1], [1, 0]]
        test_apples = [[3, 3]]

        assert ss.check_collision(test_position, test_apples) == 1

    def test_check_collision_bottom_wall_collision(self):
        test_position = [[19, 20], [19, 19], [19, 18], [18, 18]]
        test_apples = [[3, 3]]

        assert ss.check_collision(test_position, test_apples) == 1

    def test_check_collision_right_wall_collision(self):
        test_position = [[20, 19], [19, 19], [19, 18], [18, 18]]
        test_apples = [[3, 3]]

        assert ss.check_collision(test_position, test_apples) == 1


class TestMoveSnakeGrow:
    def test_move_snake_grow_no_grow(self):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_length = 3
        test_temp_position = [[1, 0]]
        assert ss.move_snake_grow(test_length, test_position, test_temp_position.copy()) == (
            False, test_temp_position + test_position[:-1])

    def test_move_snake_grow_yes_grow(self):
        test_position = [[0, 0], [0, 1], [1, 1]]
        test_length = 4
        test_temp_position = [[1, 0]]
        assert ss.move_snake_grow(test_length, test_position, test_temp_position.copy()) == (
            True, test_temp_position + test_position)


class TestMoveSnakeMove:
    def test_move_snake_move_left(self):
        test_position = [[7, 7], [7, 6], [7, 5]]
        test_direction = 'l'
        assert ss.move_snake_move(test_direction, test_position) == [[6, 7]]

    def test_move_snake_move_down(self):
        test_position = [[7, 7], [7, 6], [7, 5]]
        test_direction = 'd'
        assert ss.move_snake_move(test_direction, test_position) == [[7, 8]]

    def test_move_snake_move_right(self):
        test_position = [[7, 7], [7, 6], [7, 5]]
        test_direction = 'r'
        assert ss.move_snake_move(test_direction, test_position) == [[8, 7]]

    def test_move_snake_move_up(self):
        test_position = [[7, 7], [7, 8], [7, 9]]
        test_direction = 'u'
        assert ss.move_snake_move(test_direction, test_position) == [[7, 6]]


class TestMoveSnakeMain:
    def test_move_snake_main_without_direction(self):
        test_position = [[7, 7], [7, 6], [7, 5]]
        test_direction = ''
        test_length = 3
        assert ss.move_snake_main(test_position.copy(), test_direction, test_length) == (False, test_position)

    @patch('super_snake.move_snake_move')
    @patch('super_snake.move_snake_grow')
    def test_move_snake_main_with_direction(self, mock_move_snake_grow, mock_move_snake_move):
        mock_move_snake_move.return_value = [[0, 0]]
        mock_move_snake_grow.return_value = (False, [[7, 7], [7, 6], [7, 5]])

        test_position = [[7, 7], [7, 6], [7, 5]]
        test_direction = 'r'
        test_length = 3
        ss.move_snake_main(test_position.copy(), test_direction, test_length)
        mock_move_snake_move.assert_called_once()
        mock_move_snake_grow.assert_called_once()


@patch('pygame.image.load')
def test_draw_background(mock_image):
    mock_blit = MagicMock()
    mock_screen = MagicMock()

    mock_screen.blit = mock_blit
    test_bg_img = mock_image('Super_Snake_bg.png')

    ss.draw_background(mock_screen, test_bg_img)
    mock_blit.assert_called_once()


@patch('pygame.font.Font')
@patch('pygame.draw')
def test_draw_scoreboard_draw_score_area(mock_draw, mock_font):
    mock_screen = MagicMock()
    mock_render = MagicMock()
    mock_blit = MagicMock()
    mock_rect = MagicMock()

    test_length = 10

    mock_draw.rect.return_value = mock_rect
    mock_screen.blit = mock_blit
    mock_font.render.return_value = mock_render
    test_font = mock_font('')

    ss.draw_scoreboard(mock_screen, test_font, test_length)
    mock_draw.rect.assert_called_once()


@patch('pygame.font.Font')
@patch('pygame.draw')
def test_draw_scoreboard_draw_score_text(mock_draw, mock_font):
    mock_screen = MagicMock()
    mock_render = MagicMock()

    test_length = 10

    mock_font.render.return_value = mock_render
    test_font = mock_font('')

    ss.draw_scoreboard(mock_screen, test_font, test_length)
    mock_screen.blit.assert_called_once()


@patch('pygame.font.Font')
@patch('pygame.draw')
def test_draw_scoreboard_draw_correct_score(mock_draw, mock_font):
    mock_screen = MagicMock()
    mock_render = MagicMock()

    test_length = 10

    mock_font.render.return_value = mock_render
    test_font = mock_font('')

    ss.draw_scoreboard(mock_screen, test_font, test_length)
    test_font.render.assert_called_once_with('Score: 70', True, (255, 255, 255))


@patch('pygame.draw')
def test_draw_snake_body(mock_draw):
    mock_screen = MagicMock()
    mock_rect = MagicMock()

    test_position = [[-1, 0], [0, 0], [0, 1], [1, 0]]

    mock_draw.rect.return_value = mock_rect

    ss.draw_snake_body(mock_screen, test_position)
    mock_draw.rect.assert_called()


@patch('pygame.draw')
def test_draw_apples_one_apple(mock_draw):
    mock_screen = MagicMock()
    mock_rect = MagicMock()

    test_apples = [[1, 1]]

    mock_draw.rect.return_value = mock_rect

    ss.draw_apples(mock_screen, test_apples)
    mock_draw.rect.assert_called_once()


@patch('pygame.draw')
def test_draw_apples_multiple_apples(mock_draw):
    mock_screen = MagicMock()
    mock_rect = MagicMock()

    test_apples = [[1, 1], [3, 3]]

    mock_draw.rect.return_value = mock_rect

    ss.draw_apples(mock_screen, test_apples)
    mock_draw.rect.assert_called()
