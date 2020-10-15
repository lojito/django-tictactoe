class TicTacToe{
    static UNKNOW_PLAYER = 0;
    static USER = 1;
    static COMPUTER = 2;
    static SQUARES_NUMBER = 16;
    static LOST = "You lost the game!";
    static WON = "You won the game!";
    static TIE = "Game is a tie!";        
    
    constructor({userImagePath, computerImagePath, gameFinishUrl, gamePlayUrl}, squares, result){
        const game = this;
        this.over = false;
        this.board = Array(TicTacToe.SQUARES_NUMBER).fill(TicTacToe.UNKNOW_PLAYER);
        this.userImagePath = userImagePath;
        this.computerImagePath = computerImagePath;
        this.gameFinishUrl = gameFinishUrl;
        this.gamePlayUrl = gamePlayUrl;
        this.squares = squares;        
        this.result = result;
        
        this.squares.each(function(square){
            let backgroundImage = this.style.backgroundImage;
            if (backgroundImage.indexOf("default") !== -1){
                game.board[square] = TicTacToe.UNKNOW_PLAYER;
            } else if (backgroundImage.indexOf("user") !== -1){
                game.board[square] = TicTacToe.USER;
            } else {
                game.board[square] = TicTacToe.COMPUTER;
            }
            $(this).click(function(e){
                game.processPlay(TicTacToe.USER, this.id);
                if (!game.over){
                    $.ajax({
                      url: game.gamePlayUrl,
                      data: {
                        'board': game.board.join('')
                      },
                      dataType: 'json',
                      success(data) {
                        if (!game.checkForErrors(data)){
                            game.processPlay(TicTacToe.COMPUTER, data['square']);
                        }    
                      },
                      error(xhr, error){
                        console.debug(xhr); console.debug(error);
                      }
                    }); 
                }   
            })
        })            
    }
    
    checkForErrors(data){
        if (data.error != ''){
            this.result.text("The server responded with an error. You may not be able to continue playing at this time. Check the console log.");
            this.squares.prop('disabled', true);
            console.log(data.error);
            return true;
        }
        return false;    
    }
    
    hasWon(player){
        const board = this.board;
        return (
           (board[0]  == player && board[1]  == player && board[2]  == player && board[3]  == player) ||
           (board[4]  == player && board[5]  == player && board[6]  == player && board[7]  == player) ||
           (board[8]  == player && board[9]  == player && board[10] == player && board[11] == player) ||
           (board[12] == player && board[13] == player && board[14] == player && board[15] == player) ||
           (board[0]  == player && board[4]  == player && board[8]  == player && board[12] == player) ||
           (board[1]  == player && board[5]  == player && board[9]  == player && board[13] == player) ||
           (board[2]  == player && board[6]  == player && board[10] == player && board[14] == player) ||
           (board[3]  == player && board[7]  == player && board[11] == player && board[15] == player) ||
           (board[0]  == player && board[5]  == player && board[10] == player && board[15] == player) ||
           (board[3]  == player && board[6]  == player && board[9]  == player && board[12] == player)           
        )
    }
    
    isBoardFull(){
        return !this.board.includes(TicTacToe.UNKNOW_PLAYER);
    }
    
    updateBoard(player, index){
        this.board[index] = player;
        $(this.squares[index]).prop('disabled', true);
        const image = (player == TicTacToe.USER) ? this.userImagePath: this.computerImagePath;
        $(this.squares[index]).css("backgroundImage", "url(" + image + ")");
    }
    
    processPlay(player, index){
        this.updateBoard(player, index);
        if (this.hasWon(player)){
            this.squares.prop('disabled', true);
            this.result.text(player == TicTacToe.USER ? TicTacToe.WON : TicTacToe.LOST);
            this.over = true;
        } else if (this.isBoardFull()){
            this.result.text(TicTacToe.TIE);
            this.over = true;
        }
        const game = this;
        if (this.over){
            $.ajax({
              url: this.gameFinishUrl,
              data: {
                'board': this.board.join('')
              },
              dataType: 'json',
              success(data){
                  game.checkForErrors(data)
              }
            });                
        }
    }
}

new TicTacToe(config, $(".square"),$('#result'));