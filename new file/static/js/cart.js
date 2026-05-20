function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) {
        return parts.pop().split(";").shift();
    }
    return "";
}

function money(value) {
    return `$${Number(value).toFixed(2)}`;
}

async function postJson(url, payload) {
    const response = await fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify(payload),
    });

    if (response.redirected) {
        window.location.href = response.url;
        return null;
    }

    if (!response.ok) {
        throw new Error("Request failed");
    }

    return response.json();
}

function refreshCartSummary(payload) {
    const count = document.querySelector("#cart-count");
    const summaryCount = document.querySelector("#summary-count");
    const summaryTotal = document.querySelector("#summary-total");

    if (count) count.textContent = payload.count;
    if (summaryCount) summaryCount.textContent = payload.count;
    if (summaryTotal) summaryTotal.textContent = money(payload.total);

    payload.items.forEach((item) => {
        const row = document.querySelector(`.cart-row[data-item-id="${item.id}"]`);
        if (row) {
            row.querySelector(".line-subtotal").textContent = money(item.subtotal);
        }
    });
}

function bindAddToCart() {
    document.querySelectorAll(".add-cart-form").forEach((form) => {
        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            const feedback = form.parentElement.querySelector(".cart-feedback") || form.nextElementSibling;
            const quantityInput = form.querySelector("[name='quantity']");
            const quantity = Number(quantityInput ? quantityInput.value : 1);

            if (!Number.isInteger(quantity) || quantity < 1) {
                feedback.textContent = "Enter a valid quantity.";
                feedback.className = "cart-feedback error";
                return;
            }

            try {
                const payload = await postJson("/api/cart/add/", {
                    product_id: form.dataset.productId,
                    quantity,
                });
                if (!payload) return;
                refreshCartSummary(payload);
                feedback.textContent = "Added to cart.";
                feedback.className = "cart-feedback success";
            } catch (error) {
                feedback.textContent = "Please login before adding items.";
                feedback.className = "cart-feedback error";
            }
        });
    });
}

function bindCartPage() {
    document.querySelectorAll(".cart-row").forEach((row) => {
        const itemId = row.dataset.itemId;
        const quantity = row.querySelector(".cart-quantity");
        const remove = row.querySelector(".remove-item");

        quantity.addEventListener("change", async () => {
            const payload = await postJson("/api/cart/update/", {
                item_id: itemId,
                quantity: Number(quantity.value),
            });
            if (!payload) return;
            refreshCartSummary(payload);
            if (Number(quantity.value) < 1) row.remove();
        });

        remove.addEventListener("click", async () => {
            const payload = await postJson("/api/cart/remove/", { item_id: itemId });
            if (!payload) return;
            row.remove();
            refreshCartSummary(payload);
        });
    });
}

function bindFormValidation() {
    document.querySelectorAll(".validate-form").forEach((form) => {
        form.addEventListener("submit", (event) => {
            const invalid = Array.from(form.querySelectorAll("input")).find((input) => {
                return input.hasAttribute("required") && !input.value.trim();
            });

            if (invalid) {
                event.preventDefault();
                invalid.focus();
                invalid.reportValidity();
            }
        });
    });
}

document.addEventListener("DOMContentLoaded", () => {
    bindAddToCart();
    bindCartPage();
    bindFormValidation();
});
