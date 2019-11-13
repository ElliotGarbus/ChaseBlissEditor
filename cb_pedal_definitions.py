from dataclasses import dataclass
from typing import Sequence, Tuple


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
    left_channel: str = 'None'
    right_channel: str = 'None'
    logo: str = 'None'
    color: Tuple[float, float, float] = (0, 0, 0)


total_recall_time_division = ('Qtr', 'Dotted 8th', '8th Triplet', '8th', '8th Sextolets', '16th')
time_division = ('Whole', 'Half', 'Qtr Triplets', 'Qtr', '8th', '16th')

mood = Pedal(name='Mood',
             cc14='Gain', cc15='Freq', cc16='Volume',
             cc17='Bass', cc18='Mids', cc19='LPF',
             cc21=('Reverb', 'Delay', 'Slip'), cc22=('In -> Blood', 'In + Drolo -> Blood', 'Drolo -> Blood'),
             cc23=('Env', 'Tape', 'Stretch'),
             left_channel='Blood', right_channel='Drolo',
             logo='mood.png', color=(254/255, 144/255, 114/255))

dark_world = Pedal(name='Dark World',
                   cc14='Decay', cc15='Mix', cc16='Dwell',
                   cc17='Modify', cc18='Tone', cc19='Pre-Delay',
                   left_channel='D', right_channel='W',
                   logo='dark world.png', color=(172/255, 180/255, 191/255))

thermae = Pedal(name='Thermae',
                cc14='Mix', cc15='LPF', cc16='Regen',
                cc17='Glide', cc18='Int 1 (Speed)', cc19='Int 2 (Depth)',
                cc21=('Qtr', 'dotted 8th', '8th'), cc22=('Qtr / Smooth', 'dotted 8th / Glitchy', '8th / More Glitchy'),
                cc23=('Qtr / Tri', 'dotted 8th / Sin', '8th / Sqr'),
                cc20='Ramp', tap=True, logo='thermae.png', color=(8/255, 22/255, 49/255))

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
               left_channel='Pedal', right_channel='Drive')

brothers = Pedal(name='Brothers',
                 cc14='Gain A', cc15='Master', cc16='Gain B',
                 cc17='Tone A', cc18='Mix/Stack', cc19='Tone B',
                 left_channel='A', right_channel='B')

gravitas = Pedal(name='Gravitas',
                 cc14='Drive', cc15='Volume', cc16='Tone',
                 cc17='Rate',  cc18='Depth', cc19='Sway',
                 cc20='Ramp', cc21_offset=0,
                 cc22_disabled=True, cc23_disabled=True, cc21=time_division,
                 cc22=('NA',), cc23=('NA',), tap=True)

generation_loss = Pedal(name='Generation Loss',
                        cc14='Wow', cc15='Wet', cc16='HP',
                        cc17='Flutter', cc18='Gen', cc19='LP',
                        left_channel='Pedal', right_channel='Aux')

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
