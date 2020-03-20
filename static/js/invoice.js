$(document).on('change', '.rate', function(){
    var total = 0;
    var num = this.getAttribute('id').slice(-1);
    
    var rate = this.value;
    var qty = document.getElementById('quantity'+num).value;
    var amt = parseFloat(rate) * parseFloat(qty);
    console.log('rate function');
    document.getElementsByName('amount'+num)[0].value = String(amt);
    calculateSum();
});

$(document).on('change', '.qty', function(){
    var total = 0;
    var num = this.getAttribute('id').slice(-1);
    
    var qty = this.value;
    updateBag(qty,num);

	if(document.getElementById('Rate'+num).value!=null)
	{
		var rate = document.getElementById('Rate'+num).value;
		var amt = parseFloat(rate) * parseFloat(qty);
    	document.getElementsByName('amount'+num)[0].value = String(amt);
	}
	console.log('qty function');
    calculateSum();
    

});

$(document).on('change','.qtyBag', function() {
	var num = this.getAttribute('id').slice(-1);
	var qtyBag = this.value;

	var qty = updateKg(qtyBag,num);

	if(document.getElementById('Rate'+num).value!=null)
	{
		var rate = document.getElementById('Rate'+num).value;
		var amt = parseFloat(rate) * parseFloat(qty);
    	document.getElementsByName('amount'+num)[0].value = String(amt);
	}
	console.log('qty Bag function');
    calculateSum();
});

function updateBag(qtyKG,itemNum){
	var bags = parseFloat(qtyKG) / 25;
	document.getElementById("quantityBag"+itemNum).value = bags;
}

function updateKg(qtyKG,itemNum){
	var kgs = parseFloat(qtyKG) * 25;
	document.getElementById("quantity"+itemNum).value = kgs;	

	return kgs;
}

function calculateSum() {

	var sum = 0;
	//iterate through each textboxes and add the values
	// console.log(document.getElementsById("Amount"));
	$(".Amount").each(function() {

		//add only if the value is number
		if(!isNaN(this.value) && this.value.length!=0) {
			console.log('abcd')
			sum += parseFloat(this.value);
		}
		 console.log(sum);
	});
	//.toFixed() method will roundoff the final sum to 2 decimal places
	document.getElementById("totalAmount").value = String(sum);
}
