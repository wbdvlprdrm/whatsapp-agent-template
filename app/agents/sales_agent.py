from app.data.product import PRODUCT


class SalesAgent:
    def handle_message(self, text: str) -> dict:
        text = text.lower()

        if "precio" in text or "$" in text:
            return self._price_response()

        if "medida" in text or "tamaño" in text or "dimensión" in text:
            return self._dimensions_response()

        if "envío" in text or "entrega" in text:
            return self._delivery_response()

        if "ubicación" in text or "dirección" in text or "donde" in text:
            return self._location_response()

        if "hola" in text or "buenas" in text:
            return self._greeting_response()

        if "foto" in text or "imagen" in text:
            return self._media_response()

        return self._fallback_response()

    # ---------------- RESPUESTAS ---------------- #

    def _price_response(self) -> dict:
        return {
            "text": (
                f"💰 *Precio:* ${PRODUCT['price']} USD\n"
                "🚚 *Entrega GRATIS* hasta la puerta de tu casa.\n\n"
                "¿Deseas ver fotos 📸 o conocer las medidas?"
            ),
            "media": []
        }

    def _dimensions_response(self) -> dict:
        d = PRODUCT["dimensions"]
        return {
            "text": (
                "📐 *Medidas del estante:*\n"
                f"• {d['width_m']} m de ancho\n"
                f"• {d['height_m']} m de alto\n"
                f"• {d['depth_cm']} cm de profundidad\n\n"
                "Cuenta con *4 pisos ajustables* y soporta *más de 400 lbs por piso* 💪"
            ),
            "media": []
        }

    def _delivery_response(self) -> dict:
        return {
            "text": (
                "🚚 *Entrega a domicilio GRATIS* hasta la puerta de tu casa.\n"
                "📦 Se entrega empaquetado.\n\n"
                "👉 Si lo deseas *ya armado*, hay un pequeño cargo adicional."
            ),
            "media": []
        }

    def _location_response(self) -> dict:
        return {
            "text": (
                "📍 *Nuestra ubicación:*\n"
                f"{PRODUCT['location']}"
            ),
            "media": []
        }

    def _greeting_response(self) -> dict:
        return {
            "text": (
                "¡Hola! 😊 Gracias por escribirnos.\n\n"
                "Tenemos disponibles *estantes metálicos reforzados*, ideales para negocio o bodega.\n"
                "¿Te gustaría conocer el *precio*, las *medidas* o ver *fotos*?"
            ),
            "media": []
        }

    def _media_response(self) -> dict:
        return {
            "text": "📸 Aquí tienes fotos del estante:",
            "media": [
                "https://TU_CDN/foto1.jpg",
                "https://TU_CDN/foto2.jpg"
            ]
        }

    def _fallback_response(self) -> dict:
        return {
            "text": (
                "Gracias por tu mensaje 😊\n"
                "Puedo ayudarte con:\n"
                "• Precio 💰\n"
                "• Medidas 📐\n"
                "• Entrega 🚚\n"
                "• Ubicación 📍\n"
                "• Fotos 📸\n\n"
                "¿Qué te gustaría saber?"
            ),
            "media": []
        }
