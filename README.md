# Group_assignment

How to play:

Press A and D to move left and right. Hold down Q, W, or E to choose your ammunition and release to shoot. Aim with the mouse.
Refactoring and extending the cannon project

Things to be implemented:
1. Implement various types of projectiles.
2. Develop several target types with different movement patterns.
  ```
  class LinearMovingTargets(Target)
  class RandomMovingTargets(Target)
  class SmoothRandomMovingTargets(Target)
  class CircularMovingTargets(Target)
  ```
4. Create "bombs" that will be dropped by targets onto the cannon.
  ```
  class BombDroppingTarget(Target)
  ```
6. Implement multiple cannons that can shoot at each other
  ```
  class EnemyTank(Tank)
  ```
