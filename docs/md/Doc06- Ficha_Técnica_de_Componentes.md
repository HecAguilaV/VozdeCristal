<div align="justify">

# DOCUMENTO 06: FICHA DE COMPONENTES (MVP)

**Proyecto:** Voz de Cristal
**ID:** VC-2026-CH-BOM-01
**Objetivo:** Prototipado de hardware de bajo costo, alta penetración de señal y bajo consumo.


## 1. Unidad de Procesamiento y Comunicación (El Corazón)

### Módulo NB-IoT / LTE-M
*   **Componente:** Ej. SIM7080G o Quectel BG95 ([LCSC](https://www.lcsc.com/)).
*   **Por qué:** Diseñados para "Deep Coverage" (sótanos/interiores) y meses de batería ([GSMA NB-IoT](https://www.gsma.com/iot/resources/nb-iot-deployment-guide/)).
*   **Costo-eficiencia:** Selección de componentes estandarizados y ampliamente disponibles, facilitando la producción en volumen y la viabilidad para políticas públicas.

### Microcontrolador (MCU)
*   **Componente:** ESP32-S3 o nRF52840.
*   **Por qué:** Bajo consumo y capacidad para TinyML (IA ligera en el chip).

## 2. Sensores (La Percepción)

### Acelerómetro
*   **Componente:** LIS3DH o ADXL345.
*   **Función:** Detectar caídas, forcejeos o "jalones" violentos. (Consumo en microamperios).

### Sensor de Ritmo Cardíaco (PPG)
*   **Componente:** MAX30102 o similar.
*   **Función:** Monitoreo de frecuencia cardíaca para detectar picos de adrenalina.
*   **Nota:** Requiere contacto con piel (pulsera/dije).

## 3. Gestión de Energía (La Autonomía)

*   **Batería:** Li-Po 150mAh - 300mAh (tipo moneda/ultra-delgada).
*   **Cargador:** Pines magnéticos (estilo smartwatch) para sellado IP68.

## 4. Interfaz y Alerta (La Salida)

*   **Micrófono:** MEMS SPH0645LM4H (Audio Hi-Fi, tamaño minúsculo).
*   **Antena:** FPC integrada al chasis.


## Sostenibilidad y Comparativa Social
La inversión en hardware y conectividad es una fracción mínima frente al costo estatal de reparación judicial y terapias de por vida. El diseño costo-eficiente permite la implementación masiva sin comprometer presupuestos públicos.

---
## Fuentes y Referencias
- LCSC Electronics: [SIM7080G](https://www.lcsc.com/)
- GSMA: [NB-IoT Deployment Guide](https://www.gsma.com/iot/resources/nb-iot-deployment-guide/)
- Alibaba: [Costos de componentes](https://spanish.alibaba.com/)

</div>