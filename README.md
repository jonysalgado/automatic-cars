# Automatic-cars

![Version](https://img.shields.io/static/v1?label=Version&message=1.0.0&color=7159c1?style=for-the-badge) 
![Version](https://img.shields.io/static/v1?label=Dependence&message=pygame&color=red)

![Captura de tela de 2021-08-16 02-49-33](https://user-images.githubusercontent.com/50979367/129517174-9c2f2d84-387a-4335-b0c2-c0676e809d1f.png)

This project is a road simulation with a ton of cars (almost 1,000). Each car has a multi perceptron neural network. The learning estrategy is evolutionary strategy. So, the cars run several generations and the best continue for others generations.

I did this project with python and cython, my inspiration was this video: https://www.youtube.com/watch?v=gnfkfUQvKDw&t=346s

# Installation

To install this project is very simple! First, you need to run on your terminal:

```bash
git clone https://github.com/jonysalgado/automatic-cars.git
```

After, you need to compile some files, go to the project directory and run:

```bach
python setup.py build_ext --inplace
```
# Simulation

To run the simulation, you need to run:

```bach
python main.py
```
And that's it!

# Explanations

There are some keys that are useful for this project and I will list bellow:

* **Z** -> zoon in
* **X** -> zoon out
* **A**, **D**, **S**, **W** -> to move when you press **Z**
* **F1** -> to save the best cars

# Improvements

The cars don't learn every road, but I think that improvements on the neural net or evolutionary strategy has to be done. 


# Did you have any problem?

If you get any problem, please contact me:
jonysalgadofilho@gmail.com

If you like to contribute, please do it! I will like so much, I did this project to help me to study AI and I think that can help you, as well.