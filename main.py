from chess_com_parser import ChessComParser

parser = ChessComParser()

chess_com_url = 'https://www.chess.com/tournament/live/titled-tuesdays'

all_links = parser.get_all_titled_tuesday_links(chess_com_url)

save_folder = 'titled_tuesday_games'
for link in all_links:
    csv_link = parser.get_titled_tuesday_csv_link(link)
    if csv_link:
        parser.get_csv_file(csv_link, save_folder)
