# Group_assignment

How to play:

Press A and D to move left and right. Aim with your cursor. Hold down Q (normal), W (scatter), or E (laser) to choose your shell type and release to shoot. The longer you hold Q or W, the faster the shot. For E, you must be at maximum charge to fire, otherwise you will fire a blank instead. 

Refactoring and extending the cannon project

Things to be implemented:
1. Implement various types of projectiles.
  ```
  class Laser(GameObject)
  def strike_laser()
  def strike_scatter()
  ```
3. Develop several target types with different movement patterns.
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
