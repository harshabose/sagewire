
To determine PDB, BEC layout of SAGE. The following are considered:
## MOTORS:

The hover motor calculations are as following:

| HOVER SWEEP RESULTS | Altitude: 0m | Target Thrust: 6666g |                 | 50.40V       | <           | <         | <    | <         | 40.32V       | <           | <         | <    | <         |
| --------------------- | -------------- | ---------------------- | ----------------- | -------------- | ------------- | ----------- | ------ | ----------- | -------------- | ------------- | ----------- | ------ | ----------- |
| Motor Name          | KV           | Weight               | Propeller       | Throttle (%) | Current (A) | Power (W) | RPM  | Eff (g/W) | Throttle (%) | Current (A) | Power (W) | RPM  | Eff (g/W) |
| T-MOTOR MN1010      | 135          | 645                  | G30*10.5        | 50.10%       | 16.87       | 850.1     | 2810 | 7.84      | 62.60%       | 21.08       | 850.1     | 2810 | 7.84      |
| Vector 8020 PRO     | 120          | 565                  | VT 3010 CFRP_FP | 50.60%       | 18.59       | 937.1     | 2489 | 7.11      | 63.20%       | 23.24       | 937.1     | 2489 | 7.11      |
| Vector 8015 PRO     | 100          | 455                  | VT 3010 CFRP_FP | 57.10%       | 18.45       | 929.8     | 2522 | 7.17      | 71.40%       | 23.06       | 929.8     | 2522 | 7.17      |
| IPET N8L MANUF 48V  | 120          | 695                  | N30             | 54.50%       | 15.54       | 783.4     | 2710 | 8.51      | 68.10%       | 19.43       | 783.4     | 2710 | 8.51      |

| HOVER SWEEP RESULTS | Altitude: 1500m | Target Thrust: 6666g |                 | 50.40V       | <           | <         | <    | <         | 40.32V       | <           | <         | <    | <         |
| --------------------- | ----------------- | ---------------------- | ----------------- | -------------- | ------------- | ----------- | ------ | ----------- | -------------- | ------------- | ----------- | ------ | ----------- |
| Motor Name          | KV              | Weight               | Propeller       | Throttle (%) | Current (A) | Power (W) | RPM  | Eff (g/W) | Throttle (%) | Current (A) | Power (W) | RPM  | Eff (g/W) |
| T-MOTOR MN1010      | 135             | 645                  | G30*10.5        | 53.90%       | 18.15       | 914.7     | 3023 | 7.29      | 67.40%       | 22.69       | 914.7     | 3023 | 7.29      |
| Vector 8020 PRO     | 120             | 565                  | VT 3010 CFRP_FP | 54.40%       | 20.01       | 1008.3    | 2678 | 6.61      | 68.00%       | 25.01       | 1008.3    | 2678 | 6.61      |
| Vector 8015 PRO     | 100             | 455                  | VT 3010 CFRP_FP | 61.50%       | 19.85       | 1000.5    | 2714 | 6.66      | 76.80%       | 24.81       | 1000.5    | 2714 | 6.66      |
| IPET N8L MANUF 48V  | 120             | 695                  | N30             | 58.60%       | 16.73       | 843       | 2916 | 7.91      | 73.30%       | 20.91       | 843       | 2916 | 7.91      |

| HOVER SWEEP RESULTS | Altitude: 5000m | Target Thrust: 6666g |                 | 50.40V       | <           | <         | <    | <         | 40.32V       | <           | <         | <    | <         |
| --------------------- | ----------------- | ---------------------- | ----------------- | -------------- | ------------- | ----------- | ------ | ----------- | -------------- | ------------- | ----------- | ------ | ----------- |
| Motor Name          | KV              | Weight               | Propeller       | Throttle (%) | Current (A) | Power (W) | RPM  | Eff (g/W) | Throttle (%) | Current (A) | Power (W) | RPM  | Eff (g/W) |
| T-MOTOR MN1010      | 135             | 645                  | G30*10.5        | 64.60%       | 21.76       | 1096.6    | 3624 | 6.08      | 80.80%       | 27.2        | 1096.6    | 3624 | 6.08      |
| Vector 8020 PRO     | 120             | 565                  | VT 3010 CFRP_FP | 65.20%       | 23.98       | 1208.8    | 3211 | 5.51      | 81.50%       | 29.98       | 1208.8    | 3211 | 5.51      |
| Vector 8015 PRO     | 100             | 455                  | VT 3010 CFRP_FP | 73.70%       | 23.8        | 1199.4    | 3254 | 5.56      | 92.10%       | 29.75       | 1199.4    | 3254 | 5.56      |
| IPET N8L MANUF 48V  | 120             | 695                  | N30             | 70.30%       | 20.05       | 1010.7    | 3496 | 6.6       | 87.80%       | 25.07       | 1010.7    | 3496 | 6.6       |

Scaling the max current required at higher altitudes result in over-throttling (more than 100%) for a given constant thrust requirement. Thus, the maximum current required by a motor is the maximum (100%) supported current at sea-level as following:

| VT8020PRO KV120 VT3010 CFRP_FP | <           | <               | <    | <          | <         | <                | VT8020PRO KV100 VT3010 CFRP_FP 40.32V | <           |        <        | <    | <          | <         | <                |
| :----------------------------: | ----------- | --------------- | ---- | ---------- | --------- | ---------------- | ------------------------------------- | ----------- | :-------------: | ---- | ---------- | --------- | ---------------- |
|          Throttle (%)          | Voltage (V) | Current (A)     | RPM  | Thrust (g) | Power (W) | Efficiency (g/W) | Throttle (%)                          | Voltage (V) |   Current (A)   | RPM  | Thrust (g) | Power (W) | Efficiency (g/W) |
|             29.52%             | 50.4        | 2.952380952     | 1297 | 1885       | 148.8     | 12.7             | 36.90%                                | 40.32       |   3.69047619    | 1428 | 1296.4     | 114.8     | 11.3             |
|             39.21%             | 50.4        | 7.351190476     | 1797 | 3646       | 370.5     | 9.8              | 49.01%                                | 40.32       |   9.188988095   | 1907 | 2528.5     | 253.5     | 10               |
|             48.61%             | 50.4        | 15.75           | 2343 | 6107       | 793.8     | 7.7              | 60.76%<br>                            | 40.32       |   19.6875<br>   | 2383 | 4146.6     | 480.2     | 8.6              |
|             57.62%             | 50.4        | 26.02460317     | 2775 | 8486       | 1311.6    | 6.5              | 72.02%<br>                            | 40.32       |   32.53075397   | 2781 | 5777       | 772.4     | 7.5              |
|             66.39%             | 50.4        | 36.98809524     | 3129 | 10562      | 1864.2    | 5.7              | 82.99%                                | 40.32       |   46.23511905   | 3117 | 7385.5     | 1088.2    | 6.8              |
|             74.76%             | 50.4        | 50.09047619     | 3475 | 12659      | 2524.6    | 5                | 93.45%                                | 40.32       |   62.61309524   | 3450 | 9236.8     | 1485.9    | 6.2              |
|             82.68%             | 50.4        | 63.38690476     | 3784 | 14566      | 3194.7    | 4.6              | 103.35%                               | 40.32       | **79.23363095** | 3748 | 11085.7    | 1959.1    | 5.7              |
|             86.71%             | 50.4        | 68.45238095     | 3902 | 15227      | 3450      | 4.4              | 108.38%                               | 40.32       |   85.56547619   | 3955 | 12704.2    | 2346.5    | 5.4              |
|             91.27%             | 50.4        | **68.54365079** | 3892 | 15319      | 3454.6    | 4.4              | 114.09%                               | 40.32       |   85.67956349   | 3944 | 12654.9    | 2341.8    | 5.4              |
max current for VT8020PRO with VT3010 propeller is 79.2A with 40.32V at \~100% at sea level. Rounding to 80A max and total current for hover is $4 \times 80A = 320A$. 

| VT8015PRO KV100 VT3010 CFRP_FP 50.4V | <           | <               | <    | <          | <         | <                | VT8015PRO KV100 VT3010 CFRP_FP 40.32V | <           | <               | <           | <          | <         | <                |
| :----------------------------------: | ----------- | --------------- | ---- | ---------- | --------- | ---------------- | :-----------------------------------: | ----------- | --------------- | ----------- | ---------- | --------- | ---------------- |
|             Throttle (%)             | Voltage (V) | Current (A)     | RPM  | Thrust (g) | Power (W) | Efficiency (g/W) |             Throttle (%)              | Voltage (V) | Current (A)     | RPM         | Thrust (g) | Power (W) | Efficiency (g/W) |
|                29.70%                | 50.4        | 2.27718254      | 1428 | 1296.4     | 114.8     | 11.3             |              35.36845752              | 40.32       | 2.711581743     | 1360.326162 | 1296.4     | 0.6       | 109.3595542      |
|                39.44%                | 50.4        | 5.029166667     | 1907 | 2528.5     | 253.5     | 10               |              46.96893357              | 40.32       | 5.98853903      | 1816.626044 | 2528.5     | 1         | 241.486472       |
|                49.11%                | 50.4        | 9.526785714     | 2383 | 4146.6     | 480.2     | 8.6              |              58.47490472              | 40.32       | 11.34413152     | 2270.068097 | 4146.6     | 1.6       | 457.4430132      |
|                58.57%                | 50.4        | 15.32619048     | 2781 | 5777       | 772.4     | 7.5              |              69.74461363              | 40.32       | 18.24984057     | 2649.206621 | 5777       | 2.2       | 735.7954673      |
|                67.78%                | 50.4        | 21.59206349     | 3117 | 7385.5     | 1088.2    | 6.8              |              80.70718162              | 40.32       | 25.71100215     | 2969.283365 | 7385.5     | 2.7       | 1036.629502      |
|                76.82%                | 50.4        | 29.48174603     | 3450 | 9236.8     | 1485.9    | 6.2              |              91.48073983              | 40.32       | 35.10573391     | 3286.502281 | 9236.8     | 3.3       | 1415.482243      |
|                85.53%                | 50.4        | 38.87123016     | 3748 | 11085.7    | 1959.1    | 5.7              |              101.8526522              | 40.32       | **46.28637195** | 3570.37987  | 11085.7    | 4         | 1866.256991      |
|                89.53%                | 50.4        | 46.55753968     | 3955 | 12704.2    | 2346.5    | 5.4              |              106.6133364              | 40.32       | 55.43893492     | 3767.570006 | 12704.2    | 4.5       | 2235.297856      |
|                94.25%                | 50.4        | **46.46329365** | 3944 | 12654.9    | 2341.8    | 5.4              |              112.2245646              | 40.32       | 55.32671035     | 3757.091304 | 12654.9    | 4.5       | 2230.820592      |
similarly max current for VT8015PRO with VT3010 propeller is 46.4A with 40.32V. Rounding to 50A max and total current for hover is $4 \times 50A = 200A$. For forward thrust motor, max current for BH NIPPLE 6215 with GF18X10E propeller is 97.26A with 40.32V. Rounding to 100A, the total requirement is 100A.

| BH NIPPLE 6215 KV235 GF 18X10E 50.4V | <           | <           | <    | <          | <         | <                | BH NIPPLE 6215 KV235 GF 18X10E 40.32V | <           | <               | <    | <          | <         | <                |
| :----------------------------------: | ----------- | ----------- | ---- | ---------- | --------- | ---------------- | ------------------------------------- | ----------- | --------------- | ---- | ---------- | --------- | ---------------- |
|             Throttle (%)             | Voltage (V) | Current (A) | RPM  | Thrust (g) | Power (W) | Efficiency (g/W) | Throttle (%)                          | Voltage (V) | Current (A)     | RPM  | Thrust (g) | Power (W) | Efficiency (g/W) |
|                  30                  | 48.0        | 3.30        | 3148 | 1406.0     | 158.4     | 8.88             | 35.71428571                           | 40.32       | 3.928571429     | 3148 | 1406       | 158.4     | 8.88             |
|                  40                  | 48.0        | 6.00        | 3992 | 2243.0     | 288.0     | 7.79             | 47.61904762                           | 40.32       | 7.142857143     | 3992 | 2243       | 288       | 7.79             |
|                  50                  | 48.0        | 11.70       | 5024 | 3538.0     | 561.6     | 6.30             | 59.52380952                           | 40.32       | 13.92857143     | 5024 | 3538       | 561.6     | 6.3              |
|                  60                  | 48.0        | 20.05       | 5994 | 5038.0     | 984.0     | 5.12             | 71.42857143                           | 40.32       | 23.86904762     | 5994 | 5038       | 984       | 5.12             |
|                  70                  | 48.0        | 30.40       | 6728 | 6435.0     | 1459.2    | 4.41             | 83.33333333                           | 40.32       | 36.19047619     | 6728 | 6435       | 1459.2    | 4.41             |
|                  80                  | 48.0        | 44.30       | 7500 | 8101.0     | 2126.4    | 3.81             | 95.23809524                           | 40.32       | 52.73809524     | 7500 | 8101       | 2126.4    | 3.81             |
|                  90                  | 48.0        | 62.50       | 8138 | 9510.0     | 3000.0    | 3.17             | 107.1428571                           | 40.32       | **74.4047619**  | 8138 | 9510       | 3000      | 3.17             |
|                 100                  | 48.0        | **81.70**   | 8756 | 10705.0    | 3921.6    | 2.73             | 119.047619                            | 40.32       | **97.26190476** | 8756 | 10705      | 3921.6    | 2.73             |

Assuming VT8015PRO motor and BH NIPPLE 6215 combination, the max current requirement is $200A+80A = 280A$. In reality, both forward and VTOL motors won't run at the same time - but as a worse case, the combination is considered. PDB should be able to provide 300A continuous (peak actually, but worse case) current.

PDB Requirements:
	1. PDB of 300A+ continuous current with 5 ESC legs with each at least 100A output
	2. Integrated voltage and current monitoring -> telemetry to FC
	3. ~~5V BEC X2 (optional integration in PDB)~~
	4. ~~12V BEC X2 (optional integration in PDB)~~
	5. Anti-Spark Plus is needed? YES
*\* 3-5 requirements are removed as these requirements are met by the BEC layout. See [[#^afdc69|last]] of the doc*

| Attribute                    | APD PDB500X (Indian alternative Skybit PDB500X) | ==Rotoroma PDB500/ TBS Lucid 500A== | Vector Techniq PowerCore | ==AXLDrone PDB 400A==                    | ==SkyDrone SmartAP PDB400== | FT PDB X8          | PhotonDrive PDB 500 HotSwap | Mauch PL:30/8 2X200                             |
| ---------------------------- | ----------------------------------------------- | ----------------------------------- | ------------------------ | ---------------------------------------- | --------------------------- | ------------------ | --------------------------- | ----------------------------------------------- |
| Weight (g)                   | 50                                              | 44g/36g                             | 160g                     | 55g                                      | 16g                         | -                  | 60g                         | 172g (includes 2X Current Sensors 200)          |
| ESC Legs                     | 4                                               | 8                                   | 6                        | 8                                        | 12                          | 8                  | 4 (+1 maybe)                | 8                                               |
| Per ESC Max Current          | 125A                                            | 200A                                | -                        | ~~60A (website)~~ 200A (email confirmed) | -                           | -                  | 125A                        | -                                               |
| Input Voltage                | 4-14S                                           | 6S-14S                              | 6-14S                    | $\le$ 14S                                | $\le$ 14S                   | 4-12S              | 6S-15S                      | $\le$ 14S                                       |
| Cont. Current (A)            | 500A (requires 10m/s cooling)                   | 500A                                | -                        | 400A                                     | 400A                        | 300A               | 500A                        | 200A (few sources say 200A, few say 2X200=400A) |
| Peak Current (A)             | 1000A                                           | -                                   | 300A                     | 500A (email)                             |                             | -                  | -                           |                                                 |
| Require External Anti-Spark? | YES                                             | YES                                 | YES                      | NO                                       | YES                         | YES                | NO                          | NO                                              |
| 5V BEC (3A/5A)?              | 1X Partial (3A Cont.)                           | -                                   | 1X Partial (2A Cont.)    | 1X YES                                   | 1X YES                      | 1X YES (5A Cont.)  | 1X Partial (Cont. 3.5A)     | 1X YES                                          |
| 12V BEC 10A?                 | 1X Partial (3A Cont.)                           | -                                   | 1X Partial (2A Cont.)    | 1X Partial (Burst. 5A)                   | 1X Partial (Cont. 5A)       | Partial (5A Cont.) | 1X Partial (Cont. 3.5A)     | -                                               |
| Country of Origin            | Australia                                       | Czech/China                         | India                    | India                                    | UK                          | Israeli            | Europe (Difficult to order) | China                                           |


As most of the requirements are already met by [[#^afdc69|BEC Layout]], the only requirement to meet is **PDB of 300A+ continuous current with 5 ESC legs with each at least 100A output** and **Internal MOSFETS for soft-start or External anti-spark switch**.

From above list, the simplest option is TBS Lucid 500A but the manufacturing is in China. Apart from TBS, AXLDrone PDB is the second ideal option. The only issue is that the rated per ESC current is just 60A. This is fine for VTOL motors but, not for forward motor which require at max 80A. As there are 8 ESC legs on the PDB, two can be parallel connected for the forward motor. This will be confirmed with AXLDrones if this is recommended or not. Next, similar to AXLDrone, SkyDrone SmartAP PDB also has similar features and form factor. SkyDrones haven't mention about per ESC legs - this will be confirmed with the company.

## BEC Layout

^afdc69

Rated voltages and current for all avionics are:

| Sr. No | Avionics                            | Voltage Range (Direct/Indirect) (V) | Current (A)          | Supply    |
| ------ | ----------------------------------- | ----------------------------------- | -------------------- | --------- |
| 1      | Cube Orange Plus                    | 5.5V                                | 2.5A                 | 5V BEC 1  |
| 2      | Airspeed Sensor                     | 4.5V - 5.5V (CAN)                   | 50 mA                | Cube      |
| 3      | SF30/D LiDAR                        | 4.5V - 5.5V (Serial)                | 220mA max            | Cube      |
| 4      | TEVM-AR0234 Mono Camera             | 3.3V (40pin MIPI to Jetson Orin)    | ~300mA               | Jetson    |
| 5      | Sierra Precision Pro X2             | 5V\* (CAN)                          | 250mA X 2 = 500A max | Cube      |
| 6      | StrobeIT Anti-Collision Drone Light | 5V\* (and PWM Signal)               | 800mA X 4 = 3.2A max | 5V BEC 2  |
| 7      | #todo servos                        | 12V                                 |                      | 12V BEC 1 |
| 8      | Jetson Orin Nano                    | 9V-19V                              | 7A                   | 12V BEC 2 |
| 9      | 3-axis Camera                       | 11V-25.2V                           | 1A max               | 12V BEC 2 |
| 10     | #todo RF Air Unit                   |                                     |                      |           |
*\* spec show 5V (regulated); can we use 5.3V?*

| Sr. No                           | Jetson IO-BASE-B Peripherals | Max Power Draw (W)                |
| -------------------------------- | ---------------------------- | --------------------------------- |
| 1                                | Jetson Orin Nano/NX Module   | 25W/40W (Super)                   |
| 2                                | NVMe SSD PCIe Gen3           | 6W\*                              |
| 3                                | USB3.2 Gen2 x3               | 4.5W X 3 = 13.5W\**               |
| 4                                | USB2.0                       | 4.5W                              |
| 5                                | RJ45 2.5G Ethernet           | 2W\*                              |
| 6                                | RJ45 Gigabit Ethernet        | 2W\*                              |
| 7                                | 22-pin CSI Camera            | 1W\*                              |
| 8                                | 4PIN PWM fan                 | 2W                                |
| 9                                | GSM Module                   | 12.5W (peak, 2.5A,2.8A @5V,4.4V)+ |
| TOTAL MAX POWER DRAW (W)         | <                            | 83.5W (worse-case)                |
| TOTAL MAX CURRENT (A) (12V)      | <                            | 7A                                |
| TOTAL AVG CURRENT (A) (12V; 60W) | <                            | 5A                                |
*\* typical values - no specifications provided in IO-BASE-B spec sheet*
*\*\* Not all USB3.2 ports will be used. In fact, on SAGE, none will be used except for GSM module which is separately included in the list*
*\+ peak is much higher than typical (~6W)*

==So the required BEC are as following:==

| Sr No. | Voltage | Rated Current (A) | Name | Consumers                                             | Wattage |
| ------ | ------- | ----------------- | ---- | ----------------------------------------------------- | ------- |
| 1      | 5V      | 3A                |      | Cube (including Airspeed, LiDAR, Sierra Precision X2) | 15W     |
| 2      | 5V      | 5A                |      | StrobeIT ×4                                           | 25W     |
| 3      | 12V     | 10A               |      | Jetson + IO-BASE-B + gimbal & mono camera             | 80W     |
| 4      | 12V     | #todo             |      | Servo x 4 + RF Air                                    |         |
#todo need initial hinge moment estimates and comms team input

## Option 1: HUB-E (Not replying to mails)

Similar to Mauch, ==HUB-E (Bangalore)== is developing High Performance Cube H4 (Mauch PC: Power Cube V4). H4 has 3X 5.3V BECs and 1X 12V BEC. On their website, they allow for customisation. Emailed them to confirm (no response yet). ==All the specs, meet our BEC Voltage/Current requirements.== Following are the specs of the components used:

| Attribute            | High Performance Cube H4 |
| -------------------- | ------------------------ |
| Weight (with cables) | 102g                     |
| Input Voltage        | 4-14S                    |
| 5.3V X2              | 10A Cont. 15A Burst      |
| 12V X2               | 10A Cont. 15A Burst      |

## Option 2: KDE UBECUVC + AXLDrone PDB

AXLDrone has 5V and 12V each 4A Cont. and 5A peak. The 5V on PDB is dedicated to Cube (including sensors). Majority of power consumption comes from servos and jetson. As there are four servos, the wiring will become messy. So BECs like ==KDE Direct UBEC is considered which has dedicated (configurable voltage; using 12V setting) 6X servo pins and a 10 amp 12V output== for jetson and camera. This leaves StrobeIT x4 which will be powered using additional 5V BEC.


                         BATTERY
                            │
                  ┌───────────┴─────────┐
                  │                     │
              AXL PDB400            KDE UVC
                  │                     │
        ┌─────────┼──────┐         SET = 12 V
        │         │      │              │
        5V       12V    ESC        ┌────┴───────────┐
        │         │                │                │
        │         │                │                │
     Cube      [spare]         HIGH-CURRENT        SERVO
     3A                         10A path          outputs pins
        │                           │               │
        │                       ┌───┼───┐       ┌─┼─┼─┼─┐
        │                       │       │       │ │ │ │ │
        │                     Jetson  Gimbal    S1 S2 S3 S4
        │
   ┌───────┼────────┼────────┐
   │             │              │               │
 FC      Airspeed      SF30/D  Sierra X2 ×2

Extra 5V BEC
   │
   └── StrobeIT ×4

**KDE-UBECUVC:**

KDE-UBECUVC has selectable voltage between 5V, 6V, 8V & 12V with max continuous 120W and 216W max maximum.

![[Pasted image 20260902180215.png]]

| Voltage | Max Current | Cont. Current | Max Watt | Cont. Watt |
| ------- | ----------- | ------------- | -------- | ---------- |
| 5V      | 22A         | -             | 110W     | 120W       |
| 6V      | 22A         | 20A           | 132W     | 120W       |
| 8V      | 21A         | 15A           | 168W     | 120W       |
| ==12V== | ==18A==     | ==10A==       | ==216W== | ==120W==   |
Selecting the 12V will give a maximum current of 18A in total - including for servos and jetson. Assuming jetson will take 5A cont. (60W), leaving clean 5A cont. for servos. With KDE the servos will be limited as following:
- ==12V servo @ continuous current is limited to 1.25A each (X4)==
- ==12V servo @ max stall current is limited 2.75A each (X4)==

**StrobeIT BEC: RTS - MATEKSYS 12S Pro BEC** with a selection of 5V can support 5A matching our requirement above.
## Option 3: SVMFG

## Option 4: Independent RTS - MATEKSYS 12S Pro BEC