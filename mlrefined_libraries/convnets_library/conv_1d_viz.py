# import custom JS animator
from mlrefined_libraries.JSAnimation_slider_only import IPython_display_slider_only

# import standard plotting and animation
import matplotlib.pyplot as plt
plt.rc('text', usetex=True)
import matplotlib.animation as animation
from IPython.display import clear_output
import time
from matplotlib import gridspec

# import other packages
import numpy as np
import math
import pandas as pd


class visualizer:
    '''
    Illustrate convolution/cross-correlation of an input 1d sequence with variable length kernels.
    '''
    def __init__(self,**args):
        
        self.data_path = args['path']                       # input sequence
        
        # read Trump's job approval data (from http://www.presidency.ucsb.edu/data/popularity.php)
        df = pd.read_csv(self.data_path, delim_whitespace = True, header=None)

        # extract approval ratings
        y = np.asarray(df[2])

        # reverse the order of data (to be ascending in time)
        y = y[::-1]
        self.y = y

        
    def draw_it(self,**kwargs):
        
        num_frames = 100                       
        
        if 'num_frames' in kwargs:
            num_frames = kwargs['num_frames']
            
        
        weight = 'uniform'
        if 'weights' in kwargs and kwargs['weights']=='non-uniform':
            weight = 'non-uniform'
            
            
        # initialize figure
        fig = plt.figure(figsize = (10,4))
        artist = fig

        # create subplot with 3 panels, plot input function in center plot
        gs = gridspec.GridSpec(1, 3, width_ratios=[1,3, 1]) 
        ax1 = plt.subplot(gs[0]); ax1.axis('off');
        ax3 = plt.subplot(gs[2]); ax3.axis('off');
        ax = plt.subplot(gs[1])
        
   
        
        
        # slider (horizontal axis)
        slider = np.array(range(1,num_frames+1))
        
        print ('starting animation rendering...')
    
        
        # this subfunction padds the input sequence,
        # on the left with seq[0] and on the right with seq[-1]
        def myPadding (seq, length):
            left_padded = np.concatenate((seq[0]*np.ones(length),seq))
            right_padded = np.concatenate((left_padded,seq[-1]*np.ones(length)))
            return right_padded

        
        # subfunction for convolution/cross-correlation
        def myConvolution (seq, kernel):
            seq_size = len(seq)
            kernel_size = len(kernel)
    
            padded_seq = myPadding(seq, int((kernel_size-1)/2))
    
            conv = np.zeros(seq_size)
            for i in range(0, seq_size):
                conv[i] = np.dot(padded_seq[i:kernel_size+i], kernel)
            return conv
            
        
        # animation sub-function
        def animate(k):
            
            # clear the panel
            ax.cla()
            
            # print rendering update
            if np.mod(k+1,25) == 0:
                print ('rendering animation frame ' + str(k+1) + ' of ' + str(num_frames))
            if k == num_frames - 1:
                print ('animation rendering complete!')
                time.sleep(1.5)
                clear_output()
            
            # kernel size for the current frame 
            kernel_size = slider[k]
            half_size = int((kernel_size-1)/2)
            
            # construct the kernel
            if weight == 'non-uniform': 
                kernel = np.array(list(range(1,half_size+1)) + list(range(half_size+1,0,-1)))
            else:
                kernel = np.ones(2*half_size+1)
            
            kernel = kernel/sum(kernel)

            # compute convolution/cross-correlation for the current frame
            y_hat = myConvolution(self.y, kernel)

            # plot original sequence
            ax.plot(self.y, color = 'gray', linewidth=1)     
            
            # plot convolution/cross-correlation
            ax.plot(y_hat, color = 'red', linewidth=2.5)
               
            
            # fix viewing limits on panel
            ax.set_ylim([min(self.y)-2, max(self.y)+2])
            
            # set tickmarks
            ax.set_xticks(np.arange(0,len(self.y), 60))
            ax.set_yticks(np.arange(min(self.y)-2, max(self.y)+2, 4)) 
                
            
            # label axes
            ax.set_xlabel('$\mathrm{days\,\,elapsed}$', fontsize = 12)
            ax.set_ylabel('$\mathrm{approval\,\,ratings\,\,(\%)}$', fontsize = 12, rotation = 90, labelpad = 15)
            
            # set axis 
            ax.axhline(y=0, color='k', zorder = 0, linewidth = 0.5)
            
            
            return artist,
        
        anim = animation.FuncAnimation(fig, animate,frames=num_frames, interval=num_frames, blit=True)
        
        return(anim)


    
# this subfunction padds the input sequence,
# on the left with seq[0] and on the right with seq[-1]
def myPadding (seq, length):
    left_padded = np.concatenate((seq[0]*np.ones(length),seq))
    right_padded = np.concatenate((left_padded,seq[-1]*np.ones(length)))
    return right_padded    
    
    
# subfunction for convolution/cross-correlation
def myConvolution (seq, kernel):
    seq_size = len(seq)
    kernel_size = len(kernel)
    
    padded_seq = myPadding(seq, int((kernel_size-1)/2))
    
    conv = np.zeros(seq_size)
    for i in range(0, seq_size):
        conv[i] = np.dot(padded_seq[i:kernel_size+i], kernel)
    return conv
    
    

def plot_time_series(data_path, **kwargs):
    
    
    # read Trump's job approval data (from http://www.presidency.ucsb.edu/data/popularity.php)
    df = pd.read_csv(data_path, delim_whitespace = True, header=None)

    # extract approval ratings
    y = np.asarray(df[2])

    # reverse the order of data (to be ascending in time)
    y = y[::-1]   
    
    
    # initialize figure
    fig = plt.figure(figsize = (8,4))
    ax = fig.add_subplot(111)

    # plot data
    ax.plot(y, color = 'grey', linewidth=2)
    
    
    # plot convolution
    if 'plot_convolution' in kwargs and kwargs['plot_convolution']:
        
        # kernel size for the current frame 
        kernel_size = 40
        half_size = int((kernel_size-1)/2)
            
        # construct the kernel 
        kernel = np.array(list(range(1, half_size+1)) + list(range(half_size+1,0,-1)))
        kernel = kernel/sum(kernel)

        # compute convolution/cross-correlation for the current frame
        y_hat = myConvolution(y, kernel)    
            
        # plot convolution/cross-correlation
        ax.plot(y_hat, color = 'red', linewidth=2.5)
    
                       
    # fix viewing limits on panel
    ax.set_ylim([min(y)-2, max(y)+2])
            
    # set tickmarks
    ax.set_xticks(np.arange(0,len(y), 60))
    ax.set_yticks(np.arange(min(y)-2, max(y)+2, 4)) 
                
    # label axes
    ax.set_xlabel('$\mathrm{days\,\,elapsed}$', fontsize = 12)
    ax.set_ylabel('$\mathrm{approval\,\,ratings\,\,(\%)}$', fontsize = 12, rotation = 90, labelpad = 15)
            
    # set axis 
    ax.axhline(y=0, color='k', zorder = 0, linewidth = 0.5)
    
    
    
    