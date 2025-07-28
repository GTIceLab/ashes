import ashes_fg as af
from ashes_fg.examples import ors_buffer, cs_amp

af.fpaa.compile(ors_buffer, project_name='ors_buffer', chip_num=13)