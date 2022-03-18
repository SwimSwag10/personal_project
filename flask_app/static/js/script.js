consoleText(['Made by Justin', 'Social Network', 'Githubpeeker'], 'text',['white']);
function consoleText(words, id, colors) {
  if (colors === undefined) colors = ['#fff'];
  var visible = true;
  var con = document.getElementById('console');
  var letterCount = 1;
  var x = 1;
  var waiting = false;
  var target = document.getElementById(id)
  target.setAttribute('style', 'color:' + colors[0])
  window.setInterval(function() {

    if (letterCount === 0 && waiting === false) {
      waiting = true;
      target.innerHTML = words[0].substring(0, letterCount)
      window.setTimeout(function() {
        var usedColor = colors.shift();
        colors.push(usedColor);
        var usedWord = words.shift();
        words.push(usedWord);
        x = 1;
        target.setAttribute('style', 'color:' + colors[0])
        letterCount += x;
        waiting = false;
      }, 1000)
    } else if (letterCount === words[0].length + 1 && waiting === false) {
      waiting = true;
      window.setTimeout(function() {
        x = -1;
        letterCount += x;
        waiting = false;
      }, 1000)
    } else if (waiting === false) {
      target.innerHTML = words[0].substring(0, letterCount)
      letterCount += x;
    }
  }, 120)
  window.setInterval(function() {
    if (visible === true) {
      con.className = 'console-underscore hidden'
      visible = false;

    } else {
      con.className = 'console-underscore'

      visible = true;
    }
  }, 400)
}


// var quarters = 0;
// var dimes = 0;
// var nickels = 0;
// var pennies = 0;

// function change(cents) {
//   if (cents >= 25) {
//     quarters = Math.floor(cents / 25); // quarters
//     cents = cents % 25;
//   }
//   if (cents >= 10) {
//     dimes = Math.floor(cents / 10); // dimes
//     cents = cents % 10;
//   }
//   if (cents >= 5) {
//     nickels = Math.floor(cents / 5); // nickels
//     cents = cents % 5;
//   }
//   pennies = cents; // pennies

//   var change_ = {
//     _quarter: quarters,
//     _dimes: dimes,
//     _nickels: nickels,
//     _pennies: pennies,
//   };
//   return change_;
// }
// console.log(change(121));

// function largest(arr) {
//   for (var i=0; i<arr.length; i++) {
//     num = 0
//     if (arr[i])
//   }
// }
// largest([1,2,3,4,7,8,3,54,9]);
