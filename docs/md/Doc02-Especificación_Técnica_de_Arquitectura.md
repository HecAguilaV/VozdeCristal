<div align="justify">

# DOCUMENTO 02: ESPECIFICACIÓN TÉCNICA DE ARQUITECTURA

**Responsable:** Héctor Aguila (Arquitectura de Solución)
**ID:** VC-2026-CH-01-DOC02


## 1. Hardware (The Edge)

### Microcontrolador
**Propuesta:** SoC con soporte NB-IoT/LTE-M (ej. Simcom o Quectel).
- **Justificación:** Estos módulos permiten transmisión en bandas de baja frecuencia con alta penetración en concreto ([GSMA NB-IoT](https://www.gsma.com/iot/resources/nb-iot-deployment-guide/)).
- **Costo-eficiencia:** Selección de componentes estandarizados y ampliamente disponibles, facilitando la escalabilidad y la viabilidad para políticas públicas.

### Sensores
- **Acelerómetro:** De baja potencia para detección de impactos.
- **Sensor PPG:** Para monitoreo de frecuencia cardíaca (HRV).

### Protección
- **Certificación IP68.**
- **Encapsulado:** Resina epóxica para evitar manipulación o daño por líquidos.

## 2. Software e Inteligencia Artificial


### Algoritmo de Detección
Implementación de modelos de clasificación (**Random Forest**) en la nube para identificar patrones de pánico. El uso de IA en protección infantil está respaldado por literatura científica y experiencias internacionales (ver Anexo de Fuentes).
> *Patrón de Pánico = Taquicardia Súbita + Movimiento Defensivo.*

---
## Sostenibilidad y Escalabilidad
El diseño prioriza la viabilidad económica y la escalabilidad institucional, permitiendo su integración en protocolos de municipios y servicios de protección, con una inversión muy inferior a los costos de reparación judicial y terapias de por vida.

### Seguridad
- **Transporte:** Protocolo TLS 1.3.
- **Almacenamiento:** Encriptación AES-256 para audio almacenado.

---
## Fuentes y Referencias
- GSMA: [NB-IoT Deployment Guide](https://www.gsma.com/iot/resources/nb-iot-deployment-guide/)
- Ver Anexo de Fuentes y Referencias Técnicas
</div>