# ToTheSkies

I have developed my very first game "To the Skies." The game is coded in Python using Pygame and converted to HTML using Pygbag.

![image](https://github.com/CasualIntellectual/ToTheSkies/assets/137366044/2d64dc55-cb0b-4f4c-98da-042390cd9f7c)

It is an arcade-style shooting and vertical stroller game. In it, you control a hot air balloon and try to amass as many points as possible to achieve a high score. 

This can be done through ascending (the main method of getting points), collecting coins, and upgrading your balloon. Conversely, you lose health and points by colliding with birds and spikes. There are also clouds moving across the screen that will obscure the player's vision. The goal is to avoid such obstacles, or shoot the birds before they reach your balloon by using ammo pickups.You must also manage a gas bar, which will cause your balloon to fall once it reaches zero so the player has to collect gas can pickups to maintain being airborne.
![image](https://github.com/CasualIntellectual/ToTheSkies/assets/137366044/08dd77d4-1555-4524-bed9-aeeb3448fd1e)


The game gets progressively more difficult the higher the score, with more spikes, birds, and clouds being spawned. A miniboss will be periodically spawned every 20000 pts, will shoot bullets at the player. The four upgrades are: coin upgrade - increases value of coins; speed upgrade - increases speed and decreases gas consumption; shotgun upgrade - allows the player to fire a spread of three bullets; and health upgrade - allows the player to purchase more health. For each upgrade purchased, the cost increases so they have to prioritize different upgrades based on their playstyle.

![image](https://github.com/CasualIntellectual/ToTheSkies/assets/137366044/3d901baa-11f6-4431-8680-5e20862118d3)

The game is controlled via WASD and a computer mouse to aim. Currently there aren't plans for mobile controls but I believe it can be done.  

You can also play it on itch.io using this link: https://casualintellectual.itch.io/to-the-skies. 

I'm pretty proud of this game since I coded it almost entirely on my own and with very little direction, but evidently this has led to my code being messy and inefficient. 
I will be returning to this project to optimize it, since I have tons of global variables, repeated code, and inefficiencies.

Edit: December 04 2023 Organized Game Assets into folders using Pygame OS
