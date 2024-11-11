from  ApylabradosModule import Gameplay

def main():
  gameplay = Gameplay()
  
  gameplay.startGame()
  
  while not gameplay.end and gameplay.bagOfPawns.getTotalPawns() > 0:
    gameplay.dealPawns()
    gameplay.showMenu()
  
  if gameplay.bagOfPawns.getTotalPawns() <= 0:
    print("¡Te has quedado sin fichas en la bolsa!")
    print("Fin del juego")

  print("¡Enhorabuena! Has conseguido {} puntos en esta partida".format(gameplay.board.score))

if __name__ == "__main__":
  main()