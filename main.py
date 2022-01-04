import time
import threading
import random
from tools import find_empty, valid
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line, Rectangle, Color
from kivy.uix.label import Label
from kivy.clock import mainthread, Clock
from kivy.properties import NumericProperty, ObjectProperty


class GameOver(FloatLayout):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def quit_press(self):
		quit()
	

class Menu(FloatLayout):
	l1 = ObjectProperty()
	l2 = ObjectProperty()
	b1 = ObjectProperty()
	
	def __init__(self, *args, **kwargs):
		super(Menu, self).__init__(*args, **kwargs)
		
	def die(self):
		self.remove_widget(self.l1)
		self.remove_widget(self.l2)
		self.remove_widget(self.b1)
		self.remove_widget(self)
		

class Flayout(FloatLayout):
	current_num = NumericProperty(-1)
	menu_id = ObjectProperty()
	
	def __init__(self, *args, **kwargs):
		super(Flayout, self).__init__(*args, **kwargs)
		
		self.boards = [[
		    [7,8,0,4,0,0,1,2,0],
		    [6,0,0,0,7,5,0,0,9],
		    [0,0,0,6,0,1,0,7,8],
		    [0,0,7,0,4,0,2,6,0],
		    [0,0,1,0,5,0,9,3,0],
		    [9,0,4,0,6,0,0,0,5],
		    [0,7,0,3,0,0,0,1,2],
		    [1,2,0,0,0,7,4,0,0],
		    [0,4,9,2,0,6,0,0,7]
		],[ [ 0,0,4,0,0,0,0,6,7],
		  [3,0,0,4,7,0,0,0,5],
		  [1,5,0,8,2,0,0,0,3],
		  [0,0,6,0,0,0,0,3,1],
		  [8,0,2,1,0,5,6,0,4],
		  [4,1,0,0,0,0,9,0,0],
		  [7,0,0,0,8,0,0,4,6],
		  [6,0,0,0,1,2,0,0,0],
		  [9,3,0,0,0,0,7,1,0]]]


		self.solved_boards = [
		    [7,8,0,4,0,0,1,2,0],
		    [6,0,0,0,7,5,0,0,9],
		    [0,0,0,6,0,1,0,7,8],
		    [0,0,7,0,4,0,2,6,0],
		    [0,0,1,0,5,0,9,3,0],
		    [9,0,4,0,6,0,0,0,5],
		    [0,7,0,3,0,0,0,1,2],
		    [1,2,0,0,0,7,4,0,0],
		    [0,4,9,2,0,6,0,0,7]
		], [[2, 8, 4, 5, 9, 3, 1, 6, 7], [3, 6, 9, 4, 7, 1, 8, 2, 5], [1, 5, 7, 8, 2, 6, 4, 9, 3], [5, 7, 6, 9, 4, 8, 2, 3, 1], [8, 9, 2, 1, 3, 5, 6, 7, 4], [4, 1, 3, 2, 6, 7, 9, 5, 8], [7, 2, 1, 3, 8, 9, 5, 4, 6], [6, 4, 5, 7, 1, 2, 3, 8, 9], [9, 3, 8, 6, 5, 4, 7, 1, 2]]

		self.board_num = random.randint(0, 1)
		self.board = self.boards[self.board_num]
		self.solved_board = self.solved_boards[self.board_num]
		
		
		self.forced_solve = False
		
		self.width, self.height = 720, 1440
		
		self.labels = []
		
	
	def on_touch_down(self, touch):
		super().on_touch_down(touch)
		
		
		x, y = touch.pos[0], touch.pos[1]
		if 660 < x or 120 > x or 1190 < y or 650 > y:
			return False
		
		pos_x, pos_y = -1, 9
		while x > 120:
			x -= 60
			pos_x += 1
		while y > 650:
			y -= 60
			pos_y -= 1
		
		
		if self.current_num != -1:
			if self.board[pos_y][pos_x] == 0:
				self.board[pos_y][pos_x] = self.current_num
				self.update_numbers()
	
	def start_the_game(self):
		self.menu_id.opacity = 0
		self.display_setup()
	
	def start_solution(self):
		solving = threading.Thread(target=self.solve, args=(self.board,))
		self.forced_solve = True
		solving.start()
	
	def display_setup(self):
		with self.canvas.before:
			Color(1,1,1,1)
			Rectangle(pos=(0,0), size=(self.width, self.height))
		
		self.v_x, self.v_y = 90, 1190
		self.h_x, self.h_y = 90, 1190
		with self.canvas:
			Color(0,0,0,1)
			Line(rectangle=(90, 650, 540, 540), width=5)
			for i in range(1, 9):
				self.v_x += 60
				self.h_y -= 60
				
				if i % 3 == 0:
					thick = 5
				else:
					thick = 1
				Line(points=[self.v_x, self.v_y, self.v_x, 650], width=thick)
				Line(points=[self.h_x, self.h_y, self.h_x+540, self.h_y], width=thick)
		
		
		greeting = Label(text="Sudoku", pos=(self.width/2 - 70, 1200), size_hint=(0.2, 0.08), color=(0,0,0,1))
		self.add_widget(greeting)
		
		v_x, v_y = 15, 955
		for k, row in enumerate(self.board, start=1):
			for k1, col in enumerate(row, start=1):
				the_label = Label(text=str(col), pos=(v_x, v_y), size_hint=(0.3, 0.3), color=(0,0,0,1))
				self.labels.append(the_label)
				self.add_widget(the_label)
				
				v_x += 60
				
			
			v_x = 15
			v_y -= 60
	
	@mainthread
	def update_numbers(self, *dt):
		for k, label in enumerate(self.labels):
			row = k // 9
			label.text = str(self.board[row][k % 9])
		if self.board in self.solved_boards and self.forced_solve is False:
			self.game_over()
		
	def solve(self, bo):
		self.update_numbers()
		time.sleep(0.05)
		
		find = find_empty(bo)
		if find:
			row, col = find
		else:
			return True
		
		for i in range(1, 10):
			if valid(bo, (row, col), i):
				bo[row][col] = i
				
				if self.solve(bo):
					return True
				
				bo[row][col] = 0
	
		return False
	
	def hint(self):
		empty_slot = find_empty(self.board)
		if empty_slot:
			row, col = empty_slot
			self.board[row][col] = self.solved_board[row][col]
			self.update_numbers()
	
	def force_quit(self):
		quit()
	
	def game_over(self):
		self.add_widget(GameOver())
	
	def start_over(self):
		if self.board_num == 0:
			self.board_num = 1
			self.board = self.boards[1]
			self.solved_board = self.solved_boards[1]
		else:
			self.board_num = 0
			self.board = self.boards[0]
			self.solved_board = self.solved_boards[0]
		
		self.remove_widget(self.children[0])
		self.update_numbers()
		


class MainApp(App):
	def build(self):
		return Flayout()


if __name__ == "__main__":
	MainApp().run()
