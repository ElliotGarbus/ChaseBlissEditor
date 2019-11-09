from dataclasses import dataclass
from typing import Sequence


@dataclass
class Pedal:
    name: str
    cc14: str
    cc15: str
    cc16: str
    cc17: str
    cc18: str
    cc19: str
    cc20: str = 'None'
    cc21_offset: int = 1
    cc22_disabled: bool = False
    cc23_disabled: bool = False
    cc21: Sequence[str] = ('Left', 'Center', 'Right')
    cc22: Sequence[str] = ('Left', 'Center', 'Right')
    cc23: Sequence[str] = ('Left', 'Center', 'Right')
    tap: bool = False
    channel_select: Sequence[str] = ('None',)


total_recall_time_division = ('Qtr', 'Dotted 8th', '8th Triplet', '8th', '8th Sextolets', '16th')
time_division = ('Whole', 'Half', 'Qtr Triplets', 'Qtr', '8th', '16th')

mood = Pedal(name='Mood',
             cc14='Gain', cc15='Freq', cc16='Volume',
             cc17='Bass', cc18='Mids', cc19='LPF',
             channel_select=('Blood & Drolo', 'Blood', 'Drolo', 'Off'))

dark_world = Pedal(name='Dark World',
                   cc14='Decay', cc15='Mix', cc16='Dwell',
                   cc17='Modify', cc18='Tone', cc19='Pre-Delay',
                   channel_select=('D & W', 'D', 'W', 'Off'))

thermae = Pedal(name='Thermae',
                cc14='Mix', cc15='LPF', cc16='Regen',
                cc17='Glide', cc18='Int 1 (Speed)', cc19='Int 2 (Depth)',
                cc20='Ramp', tap=True)

tonal_recall = Pedal(name='Tonal Recall',
                     cc14='Tone', cc15='Mix', cc16='Rate',
                     cc17='Time', cc18='Regen', cc19='Depth',
                     cc20='Ramp', cc21_offset=0, cc22_disabled=True, cc23_disabled=True,
                     cc21=total_recall_time_division, cc22=('NA',), cc23=('NA',), tap=True)

warped_vinyl = Pedal(name='Warped Vinyl',
                     cc14='Tone', cc15='Lag', cc16='Mix',
                     cc17='RPM', cc18='Depth', cc19='Warp',
                     cc20='Ramp', cc21_offset=0, cc22_disabled=True, cc23_disabled=True,
                     cc21=time_division, cc22=('NA',), cc23=('NA',), tap=True)

condor = Pedal(name='Condor',
               cc14='Gain', cc15='Freq', cc16='Volume',
               cc17='Bass', cc18='Mids', cc19='LPF',
               channel_select=('Pedal & Drive', 'Pedal', 'Drive', 'Off'))

brothers = Pedal(name='Brothers',
                 cc14='Gain A', cc15='Master', cc16='Gain B',
                 cc17='Tone A', cc18='Mix/Stack', cc19='Tone B',
                 channel_select=('A & B', 'A', 'B', 'Off'))

gravitas = Pedal(name='Gravitas',
                 cc14='Drive', cc15='Volume', cc16='Tone',
                 cc17='Rate',  cc18='Depth', cc19='Sway',
                 cc20='Ramp', cc21_offset=0,
                 cc22_disabled=True, cc23_disabled=True, cc21=time_division,
                 cc22=('NA',), cc23=('NA',), tap=True)

generation_loss = Pedal(name='Generation Loss',
                        cc14='Wow', cc15='Wet', cc16='HP',
                        cc17='Flutter', cc18='Gen', cc19='LP',
                        channel_select=('Pedal & Aux', 'Pedal', 'Aux', 'Off'))

wombtome = Pedal(name='Wombtome',
                 cc14='Feed', cc15='Volume', cc16='Mix',
                 cc17='Rate', cc18='Depth', cc19='Form',
                 cc20='Ramp', cc21_offset=0,
                 cc22_disabled=True, cc23_disabled=True, cc21=time_division,
                 cc22=('NA',), cc23=('NA',), tap=True)

pedals = {'Brothers': brothers,
          'Condor': condor,
          'Dark World': dark_world,
          'Gen. Loss': generation_loss,
          'Gravitas': gravitas,
          'Mood': mood,
          'Thermae': thermae,
          'Tonal Recall': tonal_recall,
          'Warped Vinyl': warped_vinyl,
          'Wombtome': wombtome,
          }
