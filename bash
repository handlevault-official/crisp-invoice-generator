#!/bin/bash

# Crisp Invoice Generator - Automated Setup Script (Clean Corporate Financial Theme)

REPO_NAME="crisp-invoice-generator"
echo "[*] Initializing $REPO_NAME workspace..."

mkdir -p "$REPO_NAME"
cd "$REPO_NAME" || exit

if [ ! -d ".git" ]; then
    git init
    echo "[*] Initialized local Git repository."
fi

cat << 'EOF' > index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crisp Invoice Generator | HandleVault</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; color: #0f172a; padding: 20px; min-height: 100vh; }
        
        header { max-width: 900px; margin: 0 auto 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; }
        h1 { color: #0f172a; font-size: 22px; letter-spacing: -0.5px; }
        .sub-header { font-size: 12px; color: #64748b; margin-top: 2px; }
        
        .header-actions { display: flex; align-items: center; gap: 12px; }
        .kofi-link { background: #ff5e5b; color: #fff; text-decoration: none; padding: 8px 14px; border-radius: 6px; font-weight: bold; font-size: 13px; transition: background 0.2s; }
        .kofi-link:hover { background: #e04845; }
        
        .btn { background: #2563eb; color: #fff; border: none; padding: 9px 18px; border-radius: 6px; font-weight: 600; font-size: 13px; cursor: pointer; transition: background 0.2s; }
        .btn:hover { background: #1d4ed8; }
        .btn-danger { background: #ef4444; padding: 6px 10px; font-size: 12px; }
        .btn-danger:hover { background: #dc2626; }

        .container { max-width: 900px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 10px; border: 1px solid #e2e8f0; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }

        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
        .input-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
        
        label { font-size: 11px; text-transform: uppercase; color: #475569; font-weight: 700; }
        input { background: #f8fafc; border: 1px solid #cbd5e1; color: #0f172a; padding: 10px; border-radius: 6px; font-size: 13px; width: 100%; font-family: inherit; }
        input:focus { outline: none; border-color: #2563eb; background: #fff; box-shadow: 0 0 0 3px rgba(37,99,235,0.1); }

        table { width: 100%; border-collapse: collapse; margin: 24px 0; }
        th, td { padding: 12px 10px; text-align: left; border-bottom: 1px solid #e2e8f0; }
        th { color: #0f172a; font-size: 12px; font-weight: 700; text-transform: uppercase; background: #f8fafc; border-top: 1px solid #e2e8f0; border-bottom: 2px solid #cbd5e1; }

        .totals { text-align: right; margin-top: 24px; font-size: 18px; font-weight: 600; color: #0f172a; }
        .totals span { color: #16a34a; font-weight: 800; }

        footer { max-width: 900px; margin: 30px auto 0; text-align: center; font-size: 12px; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 15px; }
        footer a { color: #2563eb; text-decoration: none; font-weight: 600; }

        @media print {
            body { background: #fff; padding: 0; }
            header, footer, .no-print { display: none !important; }
            .container { border: none; box-shadow: none; padding: 0; max-width: 100%; }
            input { border: none; background: transparent; padding: 0; font-weight: 600; }
        }
    </style>
</head>
<body>

    <header class="no-print">
        <div>
            <h1>CRISP INVOICE GENERATOR</h1>
            <div class="sub-header">Clean Corporate & Minimalist Financial Dashboard</div>
        </div>
        <div class="header-actions">
            <a href="https://ko-fi.com/Handlevaultofficial" target="_blank" class="kofi-link">☕ Support on Ko-fi</a>
            <button class="btn" onclick="window.print()">Print / Save PDF</button>
        </div>
    </header>

    <div class="container">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 30px; border-bottom: 2px solid #0f172a; padding-bottom: 20px;">
            <div>
                <h2 style="font-size: 24px; font-weight: 800; color: #0f172a; letter-spacing: -0.5px;">INVOICE</h2>
                <div style="font-size: 12px; color: #64748b; margin-top: 4px;">HandleVault Studios</div>
            </div>
            <div style="text-align: right;">
                <div class="input-group" style="width: 160px; display: inline-block;">
                    <label>Invoice Number</label>
                    <input type="text" value="INV-001" style="font-weight: bold; text-align: right;">
                </div>
            </div>
        </div>

        <div class="grid-2">
            <div>
                <div class="input-group">
                    <label>From (Your Company)</label>
                    <input type="text" value="HandleVault Studios">
                </div>
                <div class="input-group">
                    <label>Billed To (Client Name)</label>
                    <input type="text" placeholder="Client Name / Business Name">
                </div>
            </div>
            <div>
                <div class="input-group">
                    <label>Issue Date</label>
                    <input type="date" id="invDate">
                </div>
                <div class="input-group">
                    <label>Payment Terms / Due Date</label>
                    <input type="text" value="Net 30 Days">
                </div>
            </div>
        </div>

        <table>
            <thead>
                <tr>
                    <th>Item Description</th>
                    <th style="width: 90px;">Qty</th>
                    <th style="width: 130px;">Price ($)</th>
                    <th style="width: 130px;">Total ($)</th>
                    <th class="no-print" style="width: 50px;"></th>
                </tr>
            </thead>
            <tbody id="itemsBody">
                <tr>
                    <td><input type="text" value="Pixel Art Asset Pack Design"></td>
                    <td><input type="number" class="qty" value="1" min="1" oninput="calculate()"></td>
                    <td><input type="number" class="price" value="150" min="0" oninput="calculate()"></td>
                    <td class="item-total" style="font-weight: 600;">$150.00</td>
                    <td class="no-print"><button class="btn btn-danger" onclick="deleteRow(this)">X</button></td>
                </tr>
            </tbody>
        </table>

        <button class="btn no-print" onclick="addRow()" style="background: #0f172a; margin-top: 4px;">+ Add Item</button>

        <div class="totals">
            Total Amount Due: <span id="grandTotal">$150.00</span>
        </div>
    </div>

    <footer class="no-print">
        Crisp Suite by <a href="https://ko-fi.com/Handlevaultofficial" target="_blank">HandleVault</a> — Clean, Fast & Single-File Utilities.
    </footer>

    <script>
        document.getElementById('invDate').valueAsDate = new Date();

        function calculate() {
            const rows = document.querySelectorAll('#itemsBody tr');
            let total = 0;
            rows.forEach(row => {
                const qty = parseFloat(row.querySelector('.qty').value) || 0;
                const price = parseFloat(row.querySelector('.price').value) || 0;
                const itemTotal = qty * price;
                row.querySelector('.item-total').textContent = '$' + itemTotal.toFixed(2);
                total += itemTotal;
            });
            document.getElementById('grandTotal').textContent = '$' + total.toFixed(2);
        }

        function addRow() {
            const tbody = document.getElementById('itemsBody');
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="text" placeholder="Item description..."></td>
                <td><input type="number" class="qty" value="1" min="1" oninput="calculate()"></td>
                <td><input type="number" class="price" value="0" min="0" oninput="calculate()"></td>
                <td class="item-total" style="font-weight: 600;">$0.00</td>
                <td class="no-print"><button class="btn btn-danger" onclick="deleteRow(this)">X</button></td>
            `;
            tbody.appendChild(tr);
            calculate();
        }

        function deleteRow(btn) {
            btn.closest('tr').remove();
            calculate();
        }
    </script>
</body>
</html>
EOF

echo "[*] Successfully updated index.html for $REPO_NAME with clean corporate theme & Ko-Fi link!"
