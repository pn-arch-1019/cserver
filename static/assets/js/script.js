$(document).ready(function(){
    // console.log("Oke!");
    
    

    $(".flip-icon").click(function(){
        $(this).closest('.question').find('.question-desc').slideToggle("slow");
    });


    $(window).scroll(function() {
        // Lấy vị trí cuộn của trang
        var scrollTop = $(window).scrollTop();
        // console.log("Vị trí cuộn hiện tại: " + scrollTop);

        // Thực hiện hành động dựa trên vị trí cuộn
        // Ví dụ: Thay đổi kiểu dáng của header khi cuộn
        if (scrollTop > 100) {
            $('.header-section').addClass('scrolled');
        } else {
            $('.header-section').removeClass('scrolled');
        }
    });

    document.getElementById("defaultOpen").click();

    const buySelectElem = document.getElementById('buy-option');
    const buyAmount = document.getElementById('buy-amount');
    const buyTransferInp = document.getElementById('buy-transfer');
    const buySubinfo = document.getElementById('buy-subinfo');

    buySelectElem.addEventListener('change', (event) => {
      const amountValue = event.target.options[event.target.selectedIndex].dataset.amount;
      const priceValue = event.target.options[event.target.selectedIndex].dataset.price;

      buySubinfo.innerHTML = `Đơn giá ${amountValue} VND/${buySelectElem.value}`;

      if (buyAmount.value != '') {
        buyTransferInp.value = parseFloat(buyAmount.value) * parseFloat(priceValue);
        if (buySelectElem.value == 'USDT') {
          buyTransferInp.value = parseFloat(buyAmount.value) * (parseFloat(priceValue) + 500);
        }
      }
    });

    buyAmount.addEventListener('input', (event) => {
      // console.log(buySelectElem.value);
      
      if (buySelectElem.value == 'BTC') {
        buyTransferInp.value = parseFloat(document.getElementById('btc-price').innerHTML) * parseFloat(event.target.value);
      } else if (buySelectElem.value == 'ETH') {
        buyTransferInp.value = parseFloat(document.getElementById('eth-price').innerHTML) * parseFloat(event.target.value);
      } else if (buySelectElem.value == 'USDT') {
        buyTransferInp.value = (parseFloat(document.getElementById('usdt-price').innerHTML) + 500) * parseFloat(event.target.value);
      } else if (buySelectElem.value == 'BNB') {
        buyTransferInp.value = parseFloat(document.getElementById('bnb-price').innerHTML) * parseFloat(event.target.value);
      } else {
        
      }
    });

    const sellSelectElem = document.getElementById('sell-option');
    const sellAmount = document.getElementById('sell-amount');
    const sellTransferInp = document.getElementById('sell-transfer');
    const sellSubinfo = document.getElementById('sell-subinfo');

    sellSelectElem.addEventListener('change', (event) => {
      const amountValue = event.target.options[event.target.selectedIndex].dataset.amount;
      const priceValue = event.target.options[event.target.selectedIndex].dataset.price;

      sellSubinfo.innerHTML = `Đơn giá ${amountValue} VND/${sellSelectElem.value}`;

      if (sellAmount.value != '') {
        sellTransferInp.value = parseFloat(sellAmount.value) * parseFloat(priceValue);
        if (sellSelectElem.value == 'USDT') {
          sellTransferInp.value = parseFloat(sellAmount.value) * (parseFloat(priceValue) - 1500);
        }
      }
    });

    sellAmount.addEventListener('input', (event) => {
      if (sellSelectElem.value == 'BTC') {
        sellTransferInp.value = parseFloat(document.getElementById('btc-price').innerHTML) * parseFloat(event.target.value);
      } else if (sellSelectElem.value == 'ETH') {
        sellTransferInp.value = parseFloat(document.getElementById('eth-price').innerHTML) * parseFloat(event.target.value);
      } else if (sellSelectElem.value == 'USDT') {
        sellTransferInp.value = (parseFloat(document.getElementById('usdt-price').innerHTML) - 1500) * parseFloat(event.target.value);
      } else if (sellSelectElem.value == 'BNB') {
        sellTransferInp.value = parseFloat(document.getElementById('bnb-price').innerHTML) * parseFloat(event.target.value);
      } else {
        
      }
    });

});


function openTab(evt, elemId) {
    var i, tabcontent, tablink;
    tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablink = document.getElementsByClassName("tablink");
  for (i = 0; i < tablink.length; i++) {
    tablink[i].className = tablink[i].className.replace(" active", "");
  }
  document.getElementById(elemId).style.display = "block";
  evt.currentTarget.className += " active";
}
