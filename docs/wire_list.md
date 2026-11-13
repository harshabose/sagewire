# Wire list

All cables in `harness/*.yaml`, with gauge, what they connect and comments. Generated from the YAML files, so regenerate it after changing them.

- **From / To** are connector IDs as drawn in each harness; the pins used are in the YAML.
- **BOM**: `no` means the wire belongs to a component (motor leads, capacitor legs, UBEC leads), so it is not bought.
- **Length**: every length is still a placeholder (0) until the layout analysis is done.
- Gauges marked as placeholder are not decided yet; the others are recommendations written into the YAML comments.

Total: 60 cables.


## actuators_system.yaml

| ID | Gauge | Wires (colours) | From | To | What it connects | BOM | Comments |
|---|---|---|---|---|---|---|---|
| W_ACT_01 | 10 AWG | 2 (RD, BK) | XT90_VTOL1_M | ESC_VTOL1_IN | VTOL motor 1 (front right) power, wing split to ESC | yes | Same 10 AWG as the fuselage side. Keep short (APD: more capacitance beyond 12 cm). 8 AWG if long or hot. |
| W_ACT_02 | 10 AWG | 2 (RD, BK) | XT90_VTOL2_M | ESC_VTOL2_IN | VTOL motor 2 (rear left) power, wing split to ESC | yes | Same 10 AWG as the fuselage side. Keep short (APD: more capacitance beyond 12 cm). 8 AWG if long or hot. |
| W_ACT_03 | 10 AWG | 2 (RD, BK) | XT90_VTOL3_M | ESC_VTOL3_IN | VTOL motor 3 (front left) power, wing split to ESC | yes | Same 10 AWG as the fuselage side. Keep short (APD: more capacitance beyond 12 cm). 8 AWG if long or hot. |
| W_ACT_04 | 10 AWG | 2 (RD, BK) | XT90_VTOL4_M | ESC_VTOL4_IN | VTOL motor 4 (rear right) power, wing split to ESC | yes | Same 10 AWG as the fuselage side. Keep short (APD: more capacitance beyond 12 cm). 8 AWG if long or hot. |
| W_ACT_05 | none (component's own leads) | 3 (YE, GN, BU) | ESC_VTOL1_PH | MOT_VTOL1 | VTOL motor 1 (front right) phase leads | no | Motor's own leads, gauge unknown (not in the listing); use 10 AWG if ever extended. Phase order only sets spin direction. |
| W_ACT_06 | none (component's own leads) | 3 (YE, GN, BU) | ESC_VTOL2_PH | MOT_VTOL2 | VTOL motor 2 (rear left) phase leads | no | Motor's own leads, gauge unknown (not in the listing); use 10 AWG if ever extended. Phase order only sets spin direction. |
| W_ACT_07 | none (component's own leads) | 3 (YE, GN, BU) | ESC_VTOL3_PH | MOT_VTOL3 | VTOL motor 3 (front left) phase leads | no | Motor's own leads, gauge unknown (not in the listing); use 10 AWG if ever extended. Phase order only sets spin direction. |
| W_ACT_08 | none (component's own leads) | 3 (YE, GN, BU) | ESC_VTOL4_PH | MOT_VTOL4 | VTOL motor 4 (rear right) phase leads | no | Motor's own leads, gauge unknown (not in the listing); use 10 AWG if ever extended. Phase order only sets spin direction. |
| W_ACT_09 | none (component's own leads) | 3 (YE, GN, BU) | ESC_FWD_PH | MOT_FWD | Forward motor phase leads | no | Motor's own leads, gauge unknown (not in the listing); use 10 AWG if ever extended. Phase order only sets spin direction. |
| W_ACT_10 | 26 AWG | 2 (RD, BK) | SPLIT_L_WING | SRV_L1_M | Left wing servo 1 power: 12 V and GND, wing plug to servo | yes | 26 AWG so it fits the M5 plug cup. Voltage drop about 1.8 V at the 2.2 A peak over 3 m one way (6 m loop). Servo takes 7-15 V. |
| W_ACT_11 | 26 AWG | 2 (YE, GN) | SPLIT_L_WING | SRV_L1_M | Left wing servo 1 CAN pair, wing plug to servo (twisted pair) | yes | Twisted pair. DB-25 CAN pins are adjacent. Servo has built-in 120 ohm termination. |
| W_ACT_12 | 26 AWG | 2 (RD, BK) | SPLIT_L_WING | SRV_L2_M | Left wing servo 2 power: 12 V and GND, wing plug to servo | yes | 26 AWG so it fits the M5 plug cup. Voltage drop about 1.8 V at the 2.2 A peak over 3 m one way (6 m loop). Servo takes 7-15 V. |
| W_ACT_13 | 26 AWG | 2 (YE, GN) | SPLIT_L_WING | SRV_L2_M | Left wing servo 2 CAN pair, wing plug to servo (twisted pair) | yes | Twisted pair. DB-25 CAN pins are adjacent. Servo has built-in 120 ohm termination. |
| W_ACT_14 | 22 AWG | 3 (RD, WH, BK) | SPLIT_L_WING | LED_L1 | Left wing LED 1 (StrobeIT-Pro): 5 V, signal, GND, wing plug to LED | yes | LED 0.8 A peak at 5 V. StrobeIT-Pro pad order is 5 V, signal, GND. |
| W_ACT_15 | 22 AWG | 3 (RD, WH, BK) | SPLIT_L_WING | LED_L2 | Left wing LED 2 (StrobeIT-Pro): 5 V, signal, GND, wing plug to LED | yes | LED 0.8 A peak at 5 V. StrobeIT-Pro pad order is 5 V, signal, GND. |
| W_ACT_16 | 22 AWG | 3 (RD, WH, BK) | SPLIT_L_WING | LED_LT | Left wing wingtip LED (StrobeIT): 5 V, signal, GND, wing plug to LED | yes | Wingtip StrobeIT: pad order is GND, signal, 5 V (mirrored vs the Pro); wired by pin so polarity is right. 0.8 A peak. |
| W_ACT_17 | 26 AWG | 3 (YE, WH, BK) | SPLIT_L_WING | ESC_VTOL3_SIG | Left wing ESC 1 (forward boom, VTOL motor 3, front left) signal: T, S, signal GND, wing plug to ESC | yes | T = telemetry, S = signal, then signal GND. Twist the trio (APD). Left ESC 1 = motor 3, ESC 2 = motor 2; right ESC 1 = motor 1, ESC 2 = motor 4. |
| W_ACT_18 | 26 AWG | 3 (YE, WH, BK) | SPLIT_L_WING | ESC_VTOL2_SIG | Left wing ESC 2 (aft boom, VTOL motor 2, rear left) signal: T, S, signal GND, wing plug to ESC | yes | T = telemetry, S = signal, then signal GND. Twist the trio (APD). Left ESC 1 = motor 3, ESC 2 = motor 2; right ESC 1 = motor 1, ESC 2 = motor 4. |
| W_ACT_19 | 26 AWG | 2 (RD, BK) | SPLIT_R_WING | SRV_R1_M | Right wing servo 1 power: 12 V and GND, wing plug to servo | yes | 26 AWG so it fits the M5 plug cup. Voltage drop about 1.8 V at the 2.2 A peak over 3 m one way (6 m loop). Servo takes 7-15 V. |
| W_ACT_20 | 26 AWG | 2 (YE, GN) | SPLIT_R_WING | SRV_R1_M | Right wing servo 1 CAN pair, wing plug to servo (twisted pair) | yes | Twisted pair. DB-25 CAN pins are adjacent. Servo has built-in 120 ohm termination. |
| W_ACT_21 | 26 AWG | 2 (RD, BK) | SPLIT_R_WING | SRV_R2_M | Right wing servo 2 power: 12 V and GND, wing plug to servo | yes | 26 AWG so it fits the M5 plug cup. Voltage drop about 1.8 V at the 2.2 A peak over 3 m one way (6 m loop). Servo takes 7-15 V. |
| W_ACT_22 | 26 AWG | 2 (YE, GN) | SPLIT_R_WING | SRV_R2_M | Right wing servo 2 CAN pair, wing plug to servo (twisted pair) | yes | Twisted pair. DB-25 CAN pins are adjacent. Servo has built-in 120 ohm termination. |
| W_ACT_23 | 22 AWG | 3 (RD, WH, BK) | SPLIT_R_WING | LED_R1 | Right wing LED 1 (StrobeIT-Pro): 5 V, signal, GND, wing plug to LED | yes | LED 0.8 A peak at 5 V. StrobeIT-Pro pad order is 5 V, signal, GND. |
| W_ACT_24 | 22 AWG | 3 (RD, WH, BK) | SPLIT_R_WING | LED_R2 | Right wing LED 2 (StrobeIT-Pro): 5 V, signal, GND, wing plug to LED | yes | LED 0.8 A peak at 5 V. StrobeIT-Pro pad order is 5 V, signal, GND. |
| W_ACT_25 | 22 AWG | 3 (RD, WH, BK) | SPLIT_R_WING | LED_RT | Right wing wingtip LED (StrobeIT): 5 V, signal, GND, wing plug to LED | yes | Wingtip StrobeIT: pad order is GND, signal, 5 V (mirrored vs the Pro); wired by pin so polarity is right. 0.8 A peak. |
| W_ACT_26 | 26 AWG | 3 (YE, WH, BK) | SPLIT_R_WING | ESC_VTOL1_SIG | Right wing ESC 1 (forward boom, VTOL motor 1, front right) signal: T, S, signal GND, wing plug to ESC | yes | T = telemetry, S = signal, then signal GND. Twist the trio (APD). Left ESC 1 = motor 3, ESC 2 = motor 2; right ESC 1 = motor 1, ESC 2 = motor 4. |
| W_ACT_27 | 26 AWG | 3 (YE, WH, BK) | SPLIT_R_WING | ESC_VTOL4_SIG | Right wing ESC 2 (aft boom, VTOL motor 4, rear right) signal: T, S, signal GND, wing plug to ESC | yes | T = telemetry, S = signal, then signal GND. Twist the trio (APD). Left ESC 1 = motor 3, ESC 2 = motor 2; right ESC 1 = motor 1, ESC 2 = motor 4. |
| W_ACT_28 | 26 AWG | 3 (YE, GN, BK) | SPLIT_L_FUS | CAN_SPL_P2 | Left wing servo 1 CAN_H, CAN_L and GND, fuselage DB-25 to CAN splitter (twist CAN_H/CAN_L) | yes | CAN_H, CAN_L (twist) and GND to splitter pins 2, 3, 4. Pin 1 (5 V) empty. GND is the same DB-25 pin as the servo power return. |
| W_ACT_29 | 26 AWG | 3 (YE, GN, BK) | SPLIT_L_FUS | CAN_SPL_P3 | Left wing servo 2 CAN_H, CAN_L and GND, fuselage DB-25 to CAN splitter (twist CAN_H/CAN_L) | yes | CAN_H, CAN_L (twist) and GND to splitter pins 2, 3, 4. Pin 1 (5 V) empty. GND is the same DB-25 pin as the servo power return. |
| W_ACT_30 | 26 AWG | 3 (YE, GN, BK) | SPLIT_R_FUS | CAN_SPL_P4 | Right wing servo 1 CAN_H, CAN_L and GND, fuselage DB-25 to CAN splitter (twist CAN_H/CAN_L) | yes | CAN_H, CAN_L (twist) and GND to splitter pins 2, 3, 4. Pin 1 (5 V) empty. GND is the same DB-25 pin as the servo power return. |
| W_ACT_31 | 26 AWG | 3 (YE, GN, BK) | SPLIT_R_FUS | CAN_SPL_P5 | Right wing servo 2 CAN_H, CAN_L and GND, fuselage DB-25 to CAN splitter (twist CAN_H/CAN_L) | yes | CAN_H, CAN_L (twist) and GND to splitter pins 2, 3, 4. Pin 1 (5 V) empty. GND is the same DB-25 pin as the servo power return. |
| W_ACT_32 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL1_A | ESC_VTOL1_CAP | Direct capacitor legs soldered: VTOL motor 1 (front right) ESC, capacitor 1 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_33 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL1_B | ESC_VTOL1_CAP | Direct capacitor legs soldered: VTOL motor 1 (front right) ESC, capacitor 2 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_34 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL2_A | ESC_VTOL2_CAP | Direct capacitor legs soldered: VTOL motor 2 (rear left) ESC, capacitor 1 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_35 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL2_B | ESC_VTOL2_CAP | Direct capacitor legs soldered: VTOL motor 2 (rear left) ESC, capacitor 2 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_36 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL3_A | ESC_VTOL3_CAP | Direct capacitor legs soldered: VTOL motor 3 (front left) ESC, capacitor 1 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_37 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL3_B | ESC_VTOL3_CAP | Direct capacitor legs soldered: VTOL motor 3 (front left) ESC, capacitor 2 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_38 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL4_A | ESC_VTOL4_CAP | Direct capacitor legs soldered: VTOL motor 4 (rear right) ESC, capacitor 1 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_39 | none (component's own leads) | 2 (RD, BK) | CAP_VTOL4_B | ESC_VTOL4_CAP | Direct capacitor legs soldered: VTOL motor 4 (rear right) ESC, capacitor 2 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_40 | none (component's own leads) | 2 (RD, BK) | CAP_FWD_A | ESC_FWD_CAP | Direct capacitor legs soldered: forward ESC, capacitor 1 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |
| W_ACT_41 | none (component's own leads) | 2 (RD, BK) | CAP_FWD_B | ESC_FWD_CAP | Direct capacitor legs soldered: forward ESC, capacitor 2 of 2 | no | Not a wire: the capacitor's own legs soldered to the ESC pads. Capacitors from the ESC box, spec not known. Two per ESC in parallel; legs as short as possible. |

## cellular_system.yaml

| ID | Gauge | Wires (colours) | From | To | What it connects | BOM | Comments |
|---|---|---|---|---|---|---|---|
| W_CEL_01 | 26 AWG | 4 (WHOG, OG, WHGN, GN) | A8M_NET | A8M_RJ45 | A8-MINI Ethernet pins to RJ45 plug. Two twisted pairs, crossover wiring (see comments). | yes | Two twisted pairs (T568B colours), crossover: camera RX pair lands on RJ45 1/2, TX pair on 3/6. Gauge is a placeholder; shield undecided. |
| W_CEL_04 | 26 AWG | 4 (RD, RD, BK, BK) | A8M_PWR | A8M_XT30_M | A8-MINI power port to XT30 male. Wires 1, 2 = power (red), 3, 4 = GND (black). | yes | Two wires per polarity: red pair to the two power pins, black pair to the two GND pins, joined at the XT30 pin. Power input is 3S-6S, needs a BEC (undecided). Gauge is a placeholder. |
| W_CEL_02 | 28 AWG | 3 (WH, GN, BK) | WAV1_EXT_F | WAV1_EXT_M | USB 2.0 data and ground for dongle 1. VBUS not wired yet. | yes | USB 2.0 data pair (twist) plus GND. VBUS not wired (dongle needs about 2 A, source undecided). Gauge is a placeholder. |
| W_CEL_03 | 28 AWG | 3 (WH, GN, BK) | WAV2_EXT_F | WAV2_EXT_M | USB 2.0 data and ground for dongle 2. VBUS not wired yet. | yes | USB 2.0 data pair (twist) plus GND. VBUS not wired (dongle needs about 2 A, source undecided). Gauge is a placeholder. |

## flight_control_system.yaml

| ID | Gauge | Wires (colours) | From | To | What it connects | BOM | Comments |
|---|---|---|---|---|---|---|---|
| W_FC_01 | 26 AWG | 6 (RD, RD, YE, BU, BK, BK) | PDB_FC_PWR | FC_POWER1 | PDB analog power output to Cube POWER1 | yes | 26 AWG is the one size both crimps take (GH 26-30, CLIK-Mate 22-26). Load well under 1 A. Two 5 V, current sense, voltage sense, two GND. |
| W_FC_02 | 26 AWG | 4 (RD, YE, GN, BK) | FC_CAN1 | GPS_CAN1_1 | Cube CAN1 to GPS. Twist CAN_H/CAN_L. | yes | GPS draws up to 250 mA. Twist CAN_H/CAN_L. GPS is not the end node (CAN_TERM = 0). |
| W_FC_03 | 26 AWG | 4 (RD, YE, GN, BK) | GPS_CAN1_2 | ARSP_CAN | GPS CAN1.2 to airspeed sensor (daisy chain). Twist CAN_H/CAN_L; long run. | yes | Daisy chain behind the GPS. About 50 mA. Expected long: keep CAN twisted, consider shielding. Airspeed pin order is assumed; far end of bus needs termination. |
| W_FC_04 | 30 AWG | 4 (RD, YE, GN, BK) | FC_GPS2 | LRF_COMM | Cube GPS2 to GRF-500 (serial). Wires: 1 5 V, 2 sensor TXD to Cube RX, 3 Cube TX to sensor RXD, 4 GND. | yes | 120 mA typical, 250 mA at start-up: about 0.17 V per metre of cable on 30 AWG, so keep short or go heavier. SUR contact range for 30 AWG unconfirmed. |
| W_FC_05 | 26 AWG | 3 (YE, GN, BK) | FC_CAN2 | CAN_SPL_P1 | Cube CAN2 to CAN splitter port 1. Twist CAN_H/CAN_L. | yes | CAN_H, CAN_L (twist) and GND to splitter port 1. 5 V pin not wired. |

## power_system.yaml

| ID | Gauge | Wires (colours) | From | To | What it connects | BOM | Comments |
|---|---|---|---|---|---|---|---|
| W_PWR_01 | 16 AWG | 2 (RD, BK) | PDB_ESC | UBEC_IN | Factory UBEC input leads | no | UBEC's own factory leads (about 0.21 m). Keep 16 AWG if extended. Placeholder pad pair ESC7 on the PDB. |
| W_PWR_02 | 22 AWG | 2 (RD, BK) | PDB_ESC | BEC5V_IN | AeroBuck-5 input | yes | Converter is 5 V / 4 A / 20 W max, so input is under about 2 A. Placeholder pad pair ESC8 on the PDB. |
| W_PWR_03 | 24 AWG | 2 (WH, BK) | PDB_SW | SW_BTN | PDB soft switch to pushbutton | yes | Plain two-wire contact; polarity does not matter. |
| W_PWR_04 | none (component's own leads) | 2 (RD, BK) | PDB_J2BAT | CAP_BAT | Capacitor leads, short as possible | no | Capacitor leads, short as possible. 220 uF 100 V capacitor across the battery bolts (J2); not yet picked. |
| W_PWR_05 | 10 AWG | 2 (RD, BK) | PDB_ESC | XT90_VTOL1_F | VTOL motor 1 (front right) power, PDB to wing split | yes | About 75-80 A at full throttle per motor; 8 AWG if the run is long or hot. Check fit on the PDB pads and XT90 cups. PDB pad pair follows the motor number. |
| W_PWR_06 | 10 AWG | 2 (RD, BK) | PDB_ESC | XT90_VTOL2_F | VTOL motor 2 (rear left) power, PDB to wing split | yes | About 75-80 A at full throttle per motor; 8 AWG if the run is long or hot. Check fit on the PDB pads and XT90 cups. PDB pad pair follows the motor number. |
| W_PWR_07 | 10 AWG | 2 (RD, BK) | PDB_ESC | XT90_VTOL3_F | VTOL motor 3 (front left) power, PDB to wing split | yes | About 75-80 A at full throttle per motor; 8 AWG if the run is long or hot. Check fit on the PDB pads and XT90 cups. PDB pad pair follows the motor number. |
| W_PWR_08 | 10 AWG | 2 (RD, BK) | PDB_ESC | XT90_VTOL4_F | VTOL motor 4 (rear right) power, PDB to wing split | yes | About 75-80 A at full throttle per motor; 8 AWG if the run is long or hot. Check fit on the PDB pads and XT90 cups. PDB pad pair follows the motor number. |
| W_PWR_09 | 10 AWG | 2 (RD, BK) | PDB_ESC | ESC_FWD_IN | Forward ESC power, PDB to ESC | yes | Expected up to about 80 A. Keep short (APD: long ESC input wires cause braking spikes). PDB pad pair ESC5. |

## rf_system.yaml

| ID | Gauge | Wires (colours) | From | To | What it connects | BOM | Comments |
|---|---|---|---|---|---|---|---|
| W_RF_01 | 28 AWG | 3 (YE, GN, BK) | FC_TELEM | RF_P3 | Cube TELEM to radio UART | yes | 3.3 V UART. Yellow = Cube TX to radio RX, green = Cube RX from radio TX. Shield or twist if the run is long or noisy. |
