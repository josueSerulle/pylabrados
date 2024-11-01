from  ApylabradosModule import Pawns, Word, Dictionary, FrequencyTable,Board

def main():
  bag_of_pawns = Pawns()
  player_pawns = Pawns()

  bag_of_pawns.createBag("DataSets/bag_of_pawns.csv")

  for _ in range(7):
    player_pawns.addPawn(bag_of_pawns.takeRandomPawn())

  print("\n=== Player Pawns ===")
  player_pawns_fq = player_pawns.getFrequency()
  player_pawns_fq.showFrequency()

  i = 0
  board = Board()
  while(i < 3):
    new_word = Word.readWord()
    new_word_frq  = new_word.getFrequency()
    new_word_frq.showFrequency()
    print(new_word)
    print(FrequencyTable.isSubset(new_word_frq, player_pawns_fq))

    x = int(input("Introduce la coordenada X: "))
    y = int(input("Introduce la coordenada Y: "))
    direction = input("Introduce la dirección (H para horizontal, V para vertical): ").upper()
    
    missing_pawns = board.getPawns(new_word, x, y, direction)
    missing_pawns_fq = missing_pawns.getFrequency()
        
    if FrequencyTable.isSubset(missing_pawns_fq, player_pawns_fq):
        print("El jugador tiene las fichas necesarias.")
        board.placeWord(player_pawns, new_word, x, y, direction)
        board.showBoard()
    else:
      print("El jugador no tiene las fichas necesarias para formar la palabra.")

    while(player_pawns.getTotalPawns() < 7):
      player_pawns.addPawn(bag_of_pawns.takeRandomPawn())

    player_pawns.showPawns()
    print(player_pawns.getTotalPawns())
    i += 1
main()