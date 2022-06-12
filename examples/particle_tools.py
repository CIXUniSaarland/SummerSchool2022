from threading import Event, Thread, Lock
from ipycanvas import Canvas, hold_canvas
from ipywidgets import Output, Button, Label
import numpy as np
from IPython.display import display
import time

class FilterCanvas:
    def __init__(self, pf, observing=False, estimator=None, trigger=None, predict=False):        
        self.out = Output()
        self.pf = pf
        self.canvas = Canvas(width=800, height=500)                
        self.mouse_x = 0.0
        self.estimator = estimator 
        self.trigger = trigger
        self.canvas.on_mouse_move(self.handle_mouse_move)
        self.observing = observing        
        self.world_lock = Lock()
        self.stop = Button(icon="stop")
        self.label = Label("")
        self.stop.on_click(self.stop_loop)
        self.stopping = Event()
        self.trigger_state = 0
        self.trigger_text = ""
        self.predict = predict
        self.stopping.clear()
        

    def stop_loop(self, event):
        self.stopping.set()        
        
    def start(self):
        Thread(target=self.simulate).start()
        
    def handle_mouse_move(self, x, y):        
        if self.stopping.is_set() or not self.observing:
            return 
        self.canvas.fill_style = "red"
        self.canvas.fill_rect(x,y,4)                        
        self.mouse_x = (x - self.canvas.width/2.0) / (self.canvas.width/2.0)        
        
       
    def draw_particles(self, particles, weights, y, color="#0000f030"):
        self.canvas.fill_style = color               
        sign = np.where(np.abs(particles[:,0])<0.5, 0, np.sign(particles[:,0]))
        x = particles[:,1] * sign * self.canvas.width/ 2.5 + self.canvas.width/2                
        self.canvas.fill_circles(x, y, 3)

    def draw_prediction(self, filter, y):        
        pf_copy = filter.copy()
        for i in range(10):
            pf_copy.update()
            pf_copy.update()
            self.draw_particles(pf_copy.particles, pf_copy.weights, y, color=f"#9060d010")

        
        
    def draw_estimator(self, probs):
        
        x = 10
        y = self.canvas.height 
        w = 50
        self.canvas.font = "12px sans-serif"
        for outcome, p in probs.items():
            h = p * self.canvas.height / 3  
            self.canvas.fill_style="green"
            self.canvas.fill_rect(x, y-h, width=w, height=h)            
            self.canvas.fill_style="black"
            self.canvas.fill_text(str(outcome), x+w/2, y-50)
            x += w + 5
        
    def draw_trigger(self, action):
        if action!="no":
            self.trigger_state = 20
            self.trigger_text = action
        if self.trigger_state>0:
            self.trigger_state -= 1
            self.canvas.fill_style="green"
            self.canvas.font = "32px sans-serif"
            self.canvas.fill_text(self.trigger_text, self.canvas.width/2, self.canvas.height/2)

    def simulate(self):
        y_pos = 0
        for i in range(1000):            
            if self.stopping.is_set():
                break
            with hold_canvas():
                particles = self.pf.original_particles
                
                if not self.observing:
                    y = np.full(len(particles), y_pos) + y_pos
                    self.draw_particles(particles, self.pf.original_weights, y)
                    y_pos += 2
                else:

                    y = np.random.normal(self.canvas.height/2, 10, len(particles))
                    self.canvas.clear()                

                    if self.estimator:                                        
                        # show bar chart
                        probs = self.estimator(particles)                    
                        self.draw_estimator(probs)
                    
                        # show triggered actions
                        if self.trigger:
                            action = self.trigger(probs)
                            self.draw_trigger(action)
                    
                    self.draw_particles(particles, self.pf.original_weights, y)   
                    # show predictions, if enabled
                    if self.predict:
                        self.draw_prediction(self.pf, y)             

                if self.observing and self.mouse_x is not None:
                    self.pf.update(np.array([self.mouse_x]))
                else:
                    self.pf.update() 
                self.mouse_x = None
                time.sleep(0.05)
          
    def draw(self):
        display(self.label)
        display(self.stop)
        display(self.out)
        display(self.canvas)
        