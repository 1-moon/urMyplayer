$(document).ready(function(){
  // Initialize Tooltip
  $('[data-toggle="tooltip"]').tooltip(); 
  
  // Add smooth scrolling to all links in navbar + footer link
  $(".navbar a, footer a[href='#myPage']").on('click', function(event) {

      // Make sure this.hash has a value before overriding default behavior
      if (this.hash !== "") {

      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
          scrollTop: $(hash).offset().top
      }, 900, function(){
  
          // Add hash (#) to URL when done scrolling (default click behavior)
          window.location.hash = hash;
      });
      } // End if
  });
})
// ===============================================================================
const deleteBid = function (bidId){
    console.log(`bid which is about to delete id ${bidId}`);
  
    // data inform(bid inform)
    let bid = {
        bidId : bidId
    }
  
    // 삭제 ajax
    fetch('/delete-bid',{
        method : 'POST',
        body : JSON.stringify(bid),
        headers: {
            "Content-Type": "application/json"
        },
    }).then((response) => response.json())
    .then(()=>{
        window.location.href = '/market'; // 새로고침
    });
}

// variable 
let modal = new bootstrap.Modal('#updateBidModal');  // bid edit modal
let updateBidId; // bid which is editing 

// bid edit, call modal function
const showUpdateBidModal = function(bidId){
    console.log(`current bid id ${bidId}`);

    // apply any change on current bid 
    updateBidId = bidId;

    // Modal show
    modal.show();
}

// bid edit function 
const updateBid = function(){

let updateClub = document.querySelector('#update-club');        // current bid from 
let updateSum = document.querySelector('#update-sum'); ;        // bid sum

    // data inform(bid inform)
    let bid = {
        bidId : updateBidId,
        club : updateClub.value,
        bid_amount: updateSum.value,
    }

    console.log(bid);
    // edit ajax
    fetch('/update-bid',{
        method : 'PUT',
        body : JSON.stringify(bid),
        headers: {
            "Content-Type": "application/json"
        },
    }).then((response) => response.json())
    .then(()=>{
        window.location.href = '/market'; // refresh
    });
}

