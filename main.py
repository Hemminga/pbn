import model


if __name__ == '__main__':
    pbn = input("Give a PBN string: ")
    # DEBUG
    if pbn == '':
       pbn = "N:Q974.KJ.QJ43.QJ8 J82.AQT4.875.K64 AT65.8532.962.A7 K3.976.AKT.T9532"
    data = model.process_pbn_input(pbn)
