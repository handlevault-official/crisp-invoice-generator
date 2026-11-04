import os, json, datetime
import pandas as pd
import streamlit as st
from invoice import build_invoice, compute

st.set_page_config(page_title="Free Invoice Generator | Handle Vault Invoice", page_icon="🧾")
home = os.environ.get("HOME_URL", "")
if home:
    st.markdown(f"[← Handle Vault]({home})")
st.title("🧾 Free Invoice Generator")
st.caption("Handle Vault Invoice: create a professional PDF invoice. Nothing is stored on the server.")

KEYS = ["biz_name", "biz_info", "accent", "currency", "payment", "notes", "tax_label", "tax"]
CUR = ["PHP", "USD", "EUR", "GBP", "AUD", "CAD", "SGD", "JPY", "INR", "AED"]

def load_profile():
    f = st.session_state.get("profile_file")
    if f is None:
        return
    try:
        data = json.loads(f.getvalue())
        for k in KEYS:
            if k not in data:
                continue
            v = float(data[k]) if k == "tax" else str(data[k])
            if k == "currency" and v not in CUR:
                continue
            st.session_state[k] = v
    except Exception:
        st.session_state["profile_bad"] = True

if st.session_state.pop("profile_bad", False):
    st.warning("That file is not a valid business profile.")

st.subheader("Your business")
c1, c2 = st.columns(2)
biz_name = c1.text_input("Business name", key="biz_name")
accent = c2.color_picker("Accent color", value="#2563eb", key="accent")
logo = st.file_uploader("Logo (optional)", type=["png", "jpg", "jpeg", "webp"])
biz_info = st.text_area("Address / contact / tax ID", key="biz_info")

st.subheader("Client")
client_name = st.text_input("Client name")
client_info = st.text_area("Client address / contact")

st.subheader("Invoice")
c1, c2, c3, c4 = st.columns(4)
number = c1.text_input("Invoice #", "INV-0001")
today = datetime.date.today()
issue = c2.date_input("Issue date", today)
due = c3.date_input("Due date", today + datetime.timedelta(days=14))
currency = c4.selectbox("Currency", CUR, key="currency")

st.subheader("Items")
df = st.data_editor(pd.DataFrame({"Description": [""], "Qty": [1.0], "Rate": [0.0]}), num_rows="dynamic", key="items")
items = []
for _, r in df.iterrows():
    d_ = "" if pd.isna(r["Description"]) else str(r["Description"]).strip()
    q = 1.0 if pd.isna(r["Qty"]) else float(r["Qty"])
    rt = 0.0 if pd.isna(r["Rate"]) else float(r["Rate"])
    if d_ or rt:
        items.append(dict(desc=d_, qty=q, rate=rt))

st.subheader("Totals")
c1, c2, c3, c4, c5 = st.columns(5)
discount = c1.number_input("Discount %", 0.0, 100.0, 0.0, step=1.0)
tax = c2.number_input("Tax %", 0.0, 100.0, 0.0, step=0.5, key="tax")
tax_label = c3.text_input("Tax name", "Tax", key="tax_label")
shipping = c4.number_input("Shipping / fees", 0.0, value=0.0)
paid = c5.number_input("Amount paid", 0.0, value=0.0)
t = compute(items, discount, tax, shipping, paid)
st.markdown(f"**Total: {currency} {t['total']:,.2f}** &nbsp;|&nbsp; Balance due: **{currency} {t['due']:,.2f}**")

payment = st.text_area("Payment details (bank, GCash, PayPal...)", key="payment")
notes = st.text_area("Notes / terms", value="Thank you for your business.", key="notes")

if st.button("Generate PDF invoice", type="primary"):
    if not items:
        st.error("Add at least one item.")
    else:
        data = dict(biz_name=(biz_name or "Your Business")[:80], biz_info=biz_info[:400], client_name=client_name[:80],
                    client_info=client_info[:400], number=(number or "INV-0001")[:30], issue=str(issue), due_date=str(due),
                    currency=currency, accent=accent, items=items, tax_label=(tax_label or "Tax")[:20], discount=discount,
                    tax=tax, shipping=shipping, paid=paid, payment=payment[:600], notes=notes[:800])
        try:
            st.session_state["inv"] = (build_invoice(data, logo.getvalue() if logo else None), data["number"])
        except Exception as e:
            st.error(f"Could not build invoice: {e}")
inv = st.session_state.get("inv")
if inv:
    st.download_button("Download PDF", inv[0], f"{inv[1]}.pdf", "application/pdf", type="primary")

with st.expander("Save or load your business details"):
    st.caption("Your details are not stored online. Download them as a small file and load it next time.")
    profile = {k: st.session_state.get(k, "") for k in KEYS}
    st.download_button("Download business profile", json.dumps(profile), "business-profile.json", "application/json")
    st.file_uploader("Load business profile", type="json", key="profile_file", on_change=load_profile)
st.divider()
st.link_button("☕ Support this tool", "https://ko-fi.com/handlevaultofficial", type="primary")
st.divider()
