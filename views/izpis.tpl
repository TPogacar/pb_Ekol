% rebase('logo_in_cas.tpl', opozorilo=opozorilo)

		<!-- Main -->
			<section id="main">

				<dl class="actions">			
					<ul><input type="submit" class="button" id="pdf" value='Prenesi PDF'/>
				</dl>

							<div class="inner">
								<div class="content">

								<!-- Elements -->
									<div class="row">
										<div>
											
											<!-- Tabela za izpis -->

			                                <div class="table-wrapper">
			                                        <!-- <table class="alt"> -->
													<table class="table table-bordered" id="tabela">

														<thead>
															<tr>
															% for stolpec in stolpci:
																<th> {{stolpec}} </th>
															% end
															</tr>
														</thead>

			                                            <!-- Vrstice -->
														<tbody>
															
															% for odpadek in odpadki:
															<tr>
																% for vrednost in odpadek:
																	<td>{{vrednost}}</td>
																% end
															</tr>
															% end
											

														</tbody>
														
													</table>
													
													
												</div>


			                            </div>
									</div>
								</div>
							</div>
						
			</section>