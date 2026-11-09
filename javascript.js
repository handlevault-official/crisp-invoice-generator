function calculateTotals() {
    // 1. Compute Subtotal from line items
    let subtotal = 0;
    // (Assuming your loop over line items adds up to subtotal)
    
    // 2. Get Discount Percentage
    const discountRate = parseFloat(document.getElementById('discountRate').value) || 0;
    const discountAmount = subtotal * (discountRate / 100);
    const discountedSubtotal = subtotal - discountAmount;

    // 3. Get Tax Rate & Compute Tax on the discounted amount
    const taxRate = parseFloat(document.getElementById('taxRate').value) || 0;
    const taxAmount = discountedSubtotal * (taxRate / 100);
    
    // 4. Compute Final Total
    const totalDue = discountedSubtotal + taxAmount;

    // Update the UI text elements accordingly
    // document.getElementById('subtotalDisplay').innerText = subtotal.toFixed(2);
    // document.getElementById('taxAmountDisplay').innerText = taxAmount.toFixed(2);
    // document.getElementById('totalDueDisplay').innerText = totalDue.toFixed(2);
}
