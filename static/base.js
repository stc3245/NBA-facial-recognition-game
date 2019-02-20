var hints = ['.hint1', '.hint2', '.hint3'];
var guess = 0

function toggle_display(){
      el = document.querySelector(hints[guess]);

      if(el.style.visibility == 'hidden'){
        el.style.visibility = 'visible'
      }
      if(guess < 2){
        guess++;
      }
}
