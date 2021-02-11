% rebase('osnova.tpl', opozorilo=opozorilo)
		
			<section id="main" class="wrapper">
				<div class="inner">
					<div class="content">

					<!-- Elements -->
						<div class="row">
							<div>

								<!-- Text -->
									<h2>Vsi odpadki</h2>

									<p>Vedno morate imeti dostop do posameznih kosov odpadkov. Ker potrebujete tudi vse 
                                    skladiščene odpadke v nekem skladišču, včasih filtrirane samo za neko klasifikacijsko 
                                    številko, lahko tukaj privzeto izpiše vse podatke o posameznem odpadku,
                                    lahko pa tudi omejite izbor izpisa.</p>

									<h4>Željeni podatki:</h4>

								    <!-- Izira stolpcov -->
									<form method="POST" action="/izpis_nekateri", name="izpis_nekateri">
										
                                        <dl class="row gtr-uniform">
                                                

                                            <!-- BREAK -->

                                            <dt class="col-3 col-12-small">
                                                <!-- skladisce -->
                                                <div> <select name="skladisce" id="skladisce" class="primary">
												    <option value="">- Skladišče -</option>
												        % from model import Skladisce
												        % for id, ime in Skladisce.skladisce():
												        	<option value={{id}}>{{ime}}</option>
												        % end
												    </select>
												</div>
                                                <br>
                                                <!-- id -->
                                                <div>
												<input type="checkbox" id="id" name='id'>
												<label for="id">ID</label>                                                
                                                <br>
                                                <!-- klas_st -->
                                                <input type="checkbox" id="klas_st" name='klas_st'>
												<label for="klas_st">Klasifikacijska številka</label>
                                                <br>
                                                <!-- naziv -->
												<input type="checkbox" id="naziv" name="naziv">
												<label for="naziv">Naziv odpadka</label>
                                                <br>
                                                <!-- teza -->
												<input type="checkbox" id="teza" name="teza">
												<label for="teza">Teža</label>
                                                <br>
                                                <!-- opomba_uvoz -->
												<input type="checkbox" id="opomba_uvoz" name="opomba_uvoz">
												<label for="opomba_uvoz">Opomba uvoza</label>
                                                <br>
                                                <!-- opomba_izvoz -->
												<input type="checkbox" id="opomba_izvoz" name="opomba_izvoz">
												<label for="opomba_izvoz">Opomba izvoza</label>
                                                <br>
                                                <!-- povzrocitelj -->
												<input type="checkbox" id="povzrocitelj" name="povzrocitelj">
												<label for="povzrocitelj">Povzročitelj</label>
                                                <br>
                                                <!-- prejemnik -->
												<input type="checkbox" id="prejemnik" name="prejemnik">
												<label for="prejemnik">Prejemnik</label>
                                                <br>
                                                <!-- dat_uvoza -->
												<input type="checkbox" id="dat_uvoza" name="dat_uvoza">
												<label for="dat_uvoza">Datum uvoza</label>
                                                <br>
                                                <!-- dat_izvoza -->
												<input type="checkbox" id="dat_izvoza" name="dat_izvoza">
												<label for="dat_izvoza">Datum izvoza</label>
                                                <br>
                                                </div>                                               
                                            

                                            <div>
                                            <input type="submit" value="Izpiši" class="primary" /><dt>
                                            </div>
                                        </dl>
									</form>


							</div>
						</div>
					</div>
				</div>
			</section>