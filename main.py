from  ApylabradosModule import Gameplay

def main():
  gameplay = Gameplay()
  
  gameplay.startGame()
  
  while not gameplay.getEnd and gameplay.getBagOfPawns.getTotalPawns() > 0:
    gameplay.dealPawns()
    gameplay.showMenu()
  
  if gameplay.getBagOfPawns.getTotalPawns() <= 0:
    print("¡Te has quedado sin fichas en la bolsa!")
    print("Fin del juego")

  print("¡Enhorabuena! Has conseguido {} puntos en esta partida".format(gameplay.getBoard.score))

if __name__ == "__main__":
  main()